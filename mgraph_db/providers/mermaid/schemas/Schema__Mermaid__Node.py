from typing                                                             import Type
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data    import Schema__Mermaid__Node__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id       import Safe_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                      import Schema__MGraph__Node

class Schema__Mermaid__Node(Schema__MGraph__Node):
    key        : Safe_Id
    label      : str
    node_data  : Schema__Mermaid__Node__Data
    node_type  : Type['Schema__Mermaid__Node']