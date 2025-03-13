from typing                                                             import List
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity    import Schema__Graph_RAG__Entity
from osbot_utils.helpers.Obj_Id                                         import Obj_Id
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe

class Schema__Graph_RAG__LLM__Entities(Type_Safe):
    entities             : List[Schema__Graph_RAG__Entity]
    llm_payload          : dict
    llm_response         : dict
    llm_request_duration : float
    llm_request_id       : Obj_Id