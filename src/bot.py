import os
from dotenv import load_dotenv
from operator import itemgetter
from langchain_community.vectorstores import redis
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain import hub
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import BaseRetriever

import chainlit as cl
from nemoguardrails import RailsConfig, LLMRails

load_dotenv(override=True)
mode: str = 'rails' if not os.getenv('MODE') else os.getenv('MODE')

def build_rails() -> LLMRails:
    config: RailsConfig = RailsConfig.from_path('./guardrails')
    rails: LLMRails = LLMRails(config, verbose=False)
    return rails

def build_chain() -> Runnable:
    retriever: BaseRetriever = redis.Redis.from_existing_index(
        OpenAIEmbeddings(model='text-embedding-3-small', dimensions=512),
        index_name=os.getenv('INDEX_NAME'),
        redis_url=os.getenv('REDIS_URL'),
        schema=os.getenv('SCHEMA')
    ).as_retriever(search_type='similarity_score_threshold', search_kwargs={'score_threshold':0.5})
    
    chain: Runnable = (
        { 'chat_history': RunnablePassthrough(), 'input': RunnablePassthrough() }
        | hub.pull("joeywhelan/rephrase")
        | ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
        | StrOutputParser()
        | RunnableParallel({ 'question': RunnablePassthrough() })
        | { 'context': itemgetter('question') | retriever, 'question': itemgetter('question') }
        | hub.pull('rlm/rag-prompt')
        | ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
        | StrOutputParser()
    )
    return chain

@cl.on_chat_start
async def on_chat_start():
    global mode
    match mode:
        case 'chain':
            cl.user_session.set('chain', build_chain())
        case 'rails':
            cl.user_session.set('rails', build_rails())
    cl.user_session.set('chat_history', [])

@cl.on_message
async def on_message(question: cl.Message):
    global mode
    chat_history: list[str] = cl.user_session.get('chat_history')
    match mode:
        case 'chain':            
            chain: Runnable = cl.user_session.get('chain')
            content = await chain.ainvoke({'chat_history': chat_history, 'input': question.content})
            answer = cl.Message(content=content)
            await answer.send()
            chat_history.append((question.content, answer.content))
            del chat_history[:-10]  
            cl.user_session.set('chat_history', chat_history)
        case 'rails':
            rails: LLMRails = cl.user_session.get('rails')
            chat_history.append({'role': 'user', 'content': question.content})
            response = await rails.generate_async(messages=chat_history)
            answer = cl.Message(content=response['content'])
            await answer.send()
            chat_history.append({'role': 'assistant', 'content': answer.content})
            del chat_history[:-10]  
            cl.user_session.set('chat_history', chat_history)