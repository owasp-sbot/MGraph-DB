from typing                                                         import Type
from mgraph_db.mgraph.schemas.identifiers.Node_Path                 import Node_Path
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data
from osbot_utils.type_safe.Type_Safe                                import Type_Safe

class Schema__MGraph__Node(Type_Safe):
    node_data : Schema__MGraph__Node__Data   = None
    node_id   : Node_Id
    node_path : Node_Path                    = None                   # Optional path identifier for string-based classification
    node_type : Type['Schema__MGraph__Node'] = None

    def __init__(self, **kwargs):
        if kwargs.get('node_id') is None:                           # make sure .node_id is set
            kwargs['node_id'] = Node_Id(Obj_Id())                   # we need to use Obj_Id() here because Node_Id() == ''
        super().__init__(**kwargs)

    def set_node_type(self, node_type=None):                         # note: this is an exception to the rule that we have no code inside schemas
        self.node_type = node_type or self.__class__                 #       this helped to handle the large number of test that failed when we changed the default of node_type to be None
        return self
