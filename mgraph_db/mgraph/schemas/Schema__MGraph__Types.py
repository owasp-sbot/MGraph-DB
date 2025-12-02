from typing                                                 import Type
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data   import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data    import Schema__MGraph__Node__Data

class Schema__MGraph__Types(Type_Safe):
    edge_type        : Type[Schema__MGraph__Edge         ] = None
    graph_data_type  : Type[Schema__MGraph__Graph__Data  ] = None
    node_type        : Type[Schema__MGraph__Node         ] = None
    node_data_type   : Type[Schema__MGraph__Node__Data   ] = None
