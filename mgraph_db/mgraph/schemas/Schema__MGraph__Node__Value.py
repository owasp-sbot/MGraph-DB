from typing                                                     import Type
from mgraph_db.mgraph.schemas.Schema__MGraph__Node              import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data import Schema__MGraph__Node__Value__Data

class Schema__MGraph__Node__Value(Schema__MGraph__Node):
    node_data : Schema__MGraph__Node__Value__Data
    node_type : Type['Schema__MGraph__Node__Value']