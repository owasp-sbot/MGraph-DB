from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity__LLM import Schema__Graph_RAG__Entity__LLM
from osbot_utils.helpers.Obj_Id                                           import Obj_Id

class Schema__Graph_RAG__Entity(Schema__Graph_RAG__Entity__LLM):
    entity_id            : Obj_Id                                                    # Unique entity identifier
    text_id              : Obj_Id           = None                                   # the ID of the text used to calculate this entity
    text_hash            : str              = None                                   # the md5_short hash of the text used o
    source_id            : Obj_Id           = None                                   # the ID of the source of the text
