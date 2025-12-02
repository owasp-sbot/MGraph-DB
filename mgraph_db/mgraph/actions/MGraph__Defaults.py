from typing                                                         import Type
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Data            import Schema__MGraph__Edge__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data           import Schema__MGraph__Graph__Data

class MGraph__Defaults(Type_Safe):                                                          # Opinionated defaults for path-mode operation

    # Schema types - opinionated for path-mode
    #node_type       : Type[Schema__MGraph__Node__Value     ]                                # Value nodes by default
    #node_data_type  : Type[Schema__MGraph__Node__Value__Data]
    node_type       : Type[Schema__MGraph__Node             ]
    node_data_type  : Type[Schema__MGraph__Node__Data       ]
    edge_type       : Type[Schema__MGraph__Edge             ]
    edge_data_type  : Type[Schema__MGraph__Edge__Data       ]
    graph_type      : Type[Schema__MGraph__Graph            ]
    graph_data_type : Type[Schema__MGraph__Graph__Data      ]

    # # Domain types
    node_domain_type: str = 'mgraph_db.mgraph.domain.Domain__MGraph__Node.Domain__MGraph__Node'     # due to circular dependencies we can't use Type[Domain__MGraph__Node]
    edge_domain_type: str = 'mgraph_db.mgraph.domain.Domain__MGraph__Edge.Domain__MGraph__Edge'     #                                       or  Type[Domain__MGraph__Edge]
    node_model_type : str = 'mgraph_db.mgraph.models.Model__MGraph__Node.Model__MGraph__Node'       #                                       or Type[Model__MGraph__Node]
    edge_model_type : str = 'mgraph_db.mgraph.models.Model__MGraph__Edge.Model__MGraph__Edge'       #                                       or Type[Model__MGraph__Edge]
