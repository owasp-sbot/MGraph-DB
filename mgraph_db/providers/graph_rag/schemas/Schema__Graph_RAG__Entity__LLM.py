from typing                                                                                 import List, Annotated
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity__Direct_Relationship   import Schema__Graph_RAG__Entity__Direct_Relationship
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity__Domain_Relationship   import Schema__Graph_RAG__Entity__Domain_Relationship
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity__Ecosystem             import Schema__Graph_RAG__Entity__Ecosystem
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe

class Schema__Graph_RAG__Entity__LLM(Type_Safe):
    confidence           : float                                                     # Confidence level (between 0 and 1)
    direct_relationships : List[Schema__Graph_RAG__Entity__Direct_Relationship]      # Relationships with other entities found in the text
    domain_relationships : List[Schema__Graph_RAG__Entity__Domain_Relationship]      # Related concepts from the broader domain knowledge
    ecosystem            : Schema__Graph_RAG__Entity__Ecosystem                      # related platforms, standards and technologies
    functional_roles     : List[str]                                                 # Specific functions/purposes (e.g., Framework, Protocol, Standard, Tool)
    name                 : str                                                       # Core entity name
    primary_domains      : List[str]                                                 # Main domains this entity belongs to (e.g., Security, Development, Infrastructure)

#confidence : Annotated[float, Min(0), Max(1)]  # not support in OpenAI structure outputs