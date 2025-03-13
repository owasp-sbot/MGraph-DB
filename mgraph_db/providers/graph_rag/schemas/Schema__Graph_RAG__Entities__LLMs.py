from typing                                                               import List
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity__LLM import Schema__Graph_RAG__Entity__LLM
from osbot_utils.type_safe.Type_Safe                                      import Type_Safe

class Schema__Graph_RAG__Entities__LLMs(Type_Safe):
    entities: List[Schema__Graph_RAG__Entity__LLM]