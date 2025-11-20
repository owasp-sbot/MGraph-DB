from typing                                                         import Type
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data
from osbot_utils.type_safe.Type_Safe                                import Type_Safe

class Schema__MGraph__Node(Type_Safe):
    node_data : Schema__MGraph__Node__Data
    node_id   : Obj_Id
    node_type : Type['Schema__MGraph__Node']

