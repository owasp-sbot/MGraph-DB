from typing                                                         import Set
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Schema__MGraph__Query__Export__View(Type_Safe):
    source_graph : Schema__MGraph__Graph
    nodes_ids    : Set[Obj_Id]
    edges_ids    : Set[Obj_Id]
