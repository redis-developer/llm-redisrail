from dotenv import load_dotenv
import os
from pathlib import Path

from nemoguardrails import LLMRails
from nemoguardrails.actions import action
from nemoguardrails.actions.actions import ActionResult

from langchain_community.vectorstores import redis
from langchain_core.retrievers import BaseRetriever
from langchain_openai import OpenAIEmbeddings
from langchain.llms.base import BaseLLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

TEMPLATE = """
      You are an assistant for question-answering tasks. 
      Use the following pieces of retrieved context to answer the question. 
      If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

      Question: {question} 
      Context:  {context}
      Answer:
"""

@action(name='rag')
async def rag(
        question: str,
        retriever: BaseRetriever,
        llm: BaseLLM
):
    rag_context = await retriever.ainvoke(question)
    context = "\n".join([doc.page_content for doc in rag_context])
    prompt = PromptTemplate.from_template(TEMPLATE)
    input = {'question': question, 'context': context}
    chain = prompt | llm | StrOutputParser()
    answer = await chain.ainvoke(input)
   
    return ActionResult(return_value=answer)

def init(app: LLMRails):
    load_dotenv(override=True)
    retriever = redis.Redis.from_existing_index(
        OpenAIEmbeddings(model="text-embedding-3-small", dimensions=512),
        index_name=os.getenv('INDEX_NAME'),
        redis_url=os.getenv('REDIS_URL'),
        schema=f'{Path.cwd()}/{os.getenv("SCHEMA")}'
    ).as_retriever(search_type='similarity_score_threshold', search_kwargs={'score_threshold':0.5})
    app.register_action_param('retriever', retriever)
    app.register_action(action=rag, name='rag')