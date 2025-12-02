from typing                                      import Type
from mgraph_db.mgraph.models.Model__MGraph__Edge import Model__MGraph__Edge
from mgraph_db.mgraph.models.Model__MGraph__Node import Model__MGraph__Node
from osbot_utils.type_safe.Type_Safe             import Type_Safe

class Model__MGraph__Types(Type_Safe):
    node_model_type: Type[Model__MGraph__Node] = None
    edge_model_type: Type[Model__MGraph__Edge] = None