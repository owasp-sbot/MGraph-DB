from typing                                                              import List, Dict, Type
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Render__Config import Schema__Mermaid__Render__Config
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Types          import Schema__Mermaid__Types
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge           import Schema__Mermaid__Edge
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph__Config  import Schema__Mermaid__Graph__Config
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node           import Schema__Mermaid__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                      import Schema__MGraph__Graph
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id         import Obj_Id

class Schema__Mermaid__Graph(Schema__MGraph__Graph):
    schema_types: Schema__Mermaid__Types
    edges        : Dict[Obj_Id, Schema__Mermaid__Edge]
    graph_data   : Schema__Mermaid__Graph__Config
    graph_type   : Type['Schema__Mermaid__Graph'     ]
    mermaid_code : List[str                          ]
    nodes        : Dict[Obj_Id, Schema__Mermaid__Node]
    render_config: Schema__Mermaid__Render__Config

