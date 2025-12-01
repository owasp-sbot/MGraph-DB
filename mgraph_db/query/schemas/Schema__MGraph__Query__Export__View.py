from typing                                                         import Set
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id


class Schema__MGraph__Query__Export__View(Type_Safe):
    source_graph : Schema__MGraph__Graph
    nodes_ids    : Set[Node_Id]
    edges_ids    : Set[Edge_Id]
