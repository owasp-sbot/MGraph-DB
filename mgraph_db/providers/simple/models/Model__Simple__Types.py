from typing                                                 import Type
from mgraph_db.mgraph.models.Model__MGraph__Types           import Model__MGraph__Types
from mgraph_db.providers.simple.models.Model__Simple__Node  import Model__Simple__Node

class Model__Simple__Types(Model__MGraph__Types):
    node_model_type: Type[Model__Simple__Node]                            # we should be able to just do this (this is a OSBot-Utils bug in the Type_Safe setter workflow