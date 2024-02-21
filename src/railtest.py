from nemoguardrails import RailsConfig, LLMRails
from dotenv import load_dotenv

load_dotenv(override=True)
config = RailsConfig.from_path('./guardrails')
rails = LLMRails(config, verbose=False)

response = rails.generate(messages=[
    {"role": "user", "content": "what effect does increasing EF_RUNTIME have?"}
])
print(response['content'])

info = rails.explain()
print('*** history ***')
print(info.colang_history)
print('*** llm calls ***')
print(info.print_llm_calls_summary())

print('*** llm call detail ***')
for call in info.llm_calls:
    print('\n*** call ***')
    print(f'prompt: {call.prompt}')
    print(f'completion: {call.completion}')