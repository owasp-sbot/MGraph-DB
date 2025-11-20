from osbot_utils.helpers.python_compatibility.python_3_8 import Annotated
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from osbot_utils.type_safe.validators.Validator__Max     import Max
from osbot_utils.type_safe.validators.Validator__Min     import Min


class Schema__Graph_RAG__Entity__Direct_Relationship(Type_Safe):
    entity            : str
    relationship_type : str
    strength          : float    # strength level (between 0 and 1)

    # strength          : Annotated[float, Min(0), Max(1)]
    # todo: add back these comments (removed then fixing the auto-generation of schema)
    # Related entity name
    # Type of relationship
    # Relationship strength (0-1)