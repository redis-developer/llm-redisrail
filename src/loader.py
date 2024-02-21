import os
from bs4 import SoupStrainer
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import redis
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

def load():
    load_dotenv(override=True)
    loader = WebBaseLoader(
        web_paths=json.loads(os.getenv('DOC_URLS')),
        bs_kwargs={'parse_only': SoupStrainer(['p'])}
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False
    )
    
    rds = redis.Redis.from_documents(
        loader.load_and_split(splitter),
        OpenAIEmbeddings(model="text-embedding-3-small", dimensions=512),
        index_name=os.getenv('INDEX_NAME'),
        key_prefix='doc',
        redis_url=os.getenv('REDIS_URL')
    ) 
    rds.write_schema(os.getenv('SCHEMA'))

if __name__ == '__main__':
    load()