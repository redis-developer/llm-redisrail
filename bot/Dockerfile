FROM python:3.10-slim
WORKDIR /bot
RUN apt-get update && apt-get upgrade
RUN apt-get -y install gcc g++
RUN pip install -qU python-dotenv redis bs4 chainlit langchain langchain_openai langchainhub nemoguardrails
COPY src/guardrails/ ./guardrails
COPY src/public src/bot.py src/chainlit.md .env redis_schema.yaml ./
EXPOSE 8000
CMD ["chainlit", "run", "bot.py", "--host=0.0.0.0", "--port=8000", "--headless"]