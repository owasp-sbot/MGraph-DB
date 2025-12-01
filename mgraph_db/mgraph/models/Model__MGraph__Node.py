from osbot_utils.type_safe.Type_Safe                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id    import Node_Id
from osbot_utils.type_safe.type_safe_core.methods.type_safe_property import set_as_property
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                   import Schema__MGraph__Node


class Model__MGraph__Node(Type_Safe):
    data    : Schema__MGraph__Node

    node_id   = set_as_property('data', 'node_id'  , Node_Id)
    node_type = set_as_property('data', 'node_type'        )  # BUG: , Type[Schema__MGraph__Node] not supported, raises "Subscripted generics cannot be used with class and instance checks" error
