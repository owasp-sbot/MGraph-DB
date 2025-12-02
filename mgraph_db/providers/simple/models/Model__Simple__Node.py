from mgraph_db.mgraph.models.Model__MGraph__Node              import Model__MGraph__Node
from mgraph_db.providers.simple.schemas.Schema__Simple__Node  import Schema__Simple__Node

class Model__Simple__Node(Model__MGraph__Node):
    data: Schema__Simple__Node
