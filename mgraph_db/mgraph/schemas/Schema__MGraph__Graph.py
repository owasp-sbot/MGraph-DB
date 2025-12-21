from typing                                                         import Dict, Type
from mgraph_db.mgraph.schemas.identifiers.Graph_Path                import Graph_Path
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Config   import Schema__MGraph__Index__Config
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Types                 import Schema__MGraph__Types
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data           import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id  import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe

class Schema__MGraph__Graph(Type_Safe):
    edges        : Dict[Edge_Id, Schema__MGraph__Edge]
    graph_data   : Schema__MGraph__Graph__Data         = None
    graph_id     : Graph_Id
    graph_path   : Graph_Path                          = None         # Optional path identifier for string-based classification
    graph_type   : Type['Schema__MGraph__Graph']       = None
    nodes        : Dict[Node_Id, Schema__MGraph__Node]
    schema_types : Schema__MGraph__Types               = None
    index_config : Schema__MGraph__Index__Config       = None         # index configuration


    def __init__(self, **kwargs):
        if kwargs.get('graph_id') is None:                          # make sure .graph_id is set
            kwargs['graph_id'] = Graph_Id(Obj_Id())                 # we need to use Obj_Id() here because Graph_Id() == ''
        super().__init__(**kwargs)

    def set_graph_type(self, graph_type=None):                      # exception to rule the Type_Safe doesn't have methods
        self.graph_type = graph_type or self.__class__
        return self