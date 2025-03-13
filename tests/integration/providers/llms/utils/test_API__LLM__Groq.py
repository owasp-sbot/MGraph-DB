from unittest                                       import TestCase


from mgraph_db.providers.llms.utils.API__LLM__Groq import ENV_NAME_GROQ__API_KEY, API__LLM__Groq, \
    GROQ__LLM_MODEL__MIXTRAL
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env                          import get_env, load_dotenv
from osbot_utils.utils.Http import POST_json
from osbot_utils.utils.Json import json_to_str
from osbot_utils.utils.Objects                      import obj


class test_API__LLM__Groq(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        if not get_env(ENV_NAME_GROQ__API_KEY):
            import pytest
            pytest.skip(f"{ENV_NAME_GROQ__API_KEY} not set")

        cls.api_llm = API__LLM__Groq()

    def test_execute(self):
        system_prompt = 'today is monday the 13 of December 2025, just reply with the exact answer'
        user_prompt   = "what is today's month?"
        payload       = { "model": GROQ__LLM_MODEL__MIXTRAL,
                          "messages": [{"role": "system", "content": system_prompt} ,
                                       {"role": "user"  , "content": user_prompt} ] }

        response       = self.api_llm.execute(payload)
        assert 'December' in obj(response).choices[0].message.content
