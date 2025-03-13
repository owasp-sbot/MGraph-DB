from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI import API__LLM__Open_AI

ENV_NAME_GROQ__API_KEY    = "GROQ__API_KEY"
GROQ__LLM_MODEL__MIXTRAL = 'Mixtral-8x7b-32768'

class API__LLM__Groq(API__LLM__Open_AI):
    api_url     : str = "https://api.groq.com/openai/v1/chat/completions"
    api_key_name: str = ENV_NAME_GROQ__API_KEY