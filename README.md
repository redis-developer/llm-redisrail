# Redis RAG with Rails
## Contents
1.  [Summary](#summary)
2.  [Architecture](#architecture)
3.  [Features](#features)
4.  [Prerequisites](#prerequisites)
5.  [Installation](#installation)
6.  [Usage](#usage)

## Summary <a name="summary"></a>
This is a demo of usage of Redis as a vector store for Retrieval Augmented Generation (RAG) in two distinct scenarios:
- Pure LangChain Expression Language (LCEL) chain with no safeguards on user or LLM interactions
- NVIDIA NeMo-Guardrails implementation restricting both user inputs and LLM outputs
Content from the Redis online documentation of Redis Vector Search is used for the RAG content.  For the Guardrails implementation, questions and answers are restricted to the topic of Redis Vector Search.

## Architecture <a name="architecture"></a>
### High-level Architecture

![architecture](https://docs.google.com/drawings/d/e/2PACX-1vTY5N2ZLu7fwy-DuFQ1T8Taf6r-jJOVOsKPlyC6I_dhxH5Y6A2lQsO3LaPYlsIPXmdl5kAfBQlBj3Z8/pub?w=976&h=354)  

### Application-level Architecture

![app](https://docs.google.com/drawings/d/e/2PACX-1vQ7uH_ho38iDeOBd8YRY1ybsVqYV41CxTYs4um6t2ytdSk7kRzKiZn9R-jE8p_0ENc65QVFI4Ta82ui/pub?w=815&h=713)
 
## Features <a name="features"></a>
- Redis Stack for the vector store
- Python Bot server (Chainlit)
- LangChain implementation of RAG with Redis
- Parallel NVIDIA NeMo-Guardrails implementation of RAG with Redis

## Prerequisites <a name="prerequisites"></a>
- Docker
- Docker Compose
- python3
- git
- pip

## Installation <a name="installation"></a>
```bash
git clone https://github.com/redis-developer/llm-redisrail.git
cd llm-redisrail
python3 -m venv .venv
source .venv/bin/activate
pip install -U python-dotenv redis bs4 langchain langchain_openai
```
- Edit the .env_template file with your OpenAI key and rename the file to .env
- By default, the guardrailed bot is executed.  If you want a non-railed bot, change the MODE variable in docker-compose to 'chain'.

## Usage <a name="usage"></a>
### Environment Start Up
```bash
start.sh
```

### Environment Shut Down
```bash
stop.sh
```
