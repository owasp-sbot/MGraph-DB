from typing                                                         import Type
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                 import Edge_Path
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Data            import Schema__MGraph__Edge__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Label           import Schema__MGraph__Edge__Label
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Schema__MGraph__Edge(Type_Safe):
    edge_id       : Edge_Id
    edge_data     : Schema__MGraph__Edge__Data   = None
    edge_type     : Type['Schema__MGraph__Edge'] = None
    edge_label    : Schema__MGraph__Edge__Label  = None
    edge_path     : Edge_Path                    = None              # Optional path identifier for string-based classification

    from_node_id  : Node_Id                      = None
    to_node_id    : Node_Id                      = None

    def __init__(self, **kwargs):
        if kwargs.get('edge_id') is None:                           # make sure .edge_id is set
            kwargs['edge_id'] = Edge_Id(Obj_Id())                   # we need to use Obj_Id() here because Edge_Id() == ''
        super().__init__(**kwargs)


    def set_edge_type(self, edge_type=None):
        self.edge_type = edge_type or self.__class__                # exception to rule the Type_Safe doesn't have methods
        return self
