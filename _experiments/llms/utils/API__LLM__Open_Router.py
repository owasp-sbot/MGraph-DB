from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI import API__LLM__Open_AI

ENV_NAME_OPEN_ROUTER__API_KEY = "OPEN_ROUTER__API_KEY"
OPEN_ROUTER__LLM_MODEL__GEMINI_2 = 'google/gemini-2.0-flash-lite-001'

class API__LLM__Open_Router(API__LLM__Open_AI):
    api_url     : str = "https://openrouter.ai/api/v1/chat/completions"
    api_key_name: str = ENV_NAME_OPEN_ROUTER__API_KEY