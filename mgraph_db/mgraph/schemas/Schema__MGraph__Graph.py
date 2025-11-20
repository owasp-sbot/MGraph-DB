from typing                                                         import Dict, Type
from mgraph_db.mgraph.schemas.Schema__MGraph__Types                 import Schema__MGraph__Types
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data           import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe

class Schema__MGraph__Graph(Type_Safe):
    edges        : Dict[Obj_Id, Schema__MGraph__Edge]
    graph_data   : Schema__MGraph__Graph__Data
    graph_id     : Obj_Id
    graph_type   : Type['Schema__MGraph__Graph']
    nodes        : Dict[Obj_Id, Schema__MGraph__Node]
    schema_types : Schema__MGraph__Types
