from typing                                          import Annotated
from osbot_utils.type_safe.Type_Safe                 import Type_Safe
from osbot_utils.type_safe.validators.Validator__Max import Max
from osbot_utils.type_safe.validators.Validator__Min import Min


class Schema__Graph_RAG__Entity__Domain_Relationship(Type_Safe):
    concept           : str
    relationship_type : str
    category          : str
    strength          : Annotated[float, Min(0), Max(1)]


 # Domain concept
 # Type of relationship
 # Category of the concept
 # Relationship strength (0-1)