from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Cache   import type_safe_cache
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node


class Schema__MGraph__Json__Node(Schema__MGraph__Node):

    def __init__(self, **kwargs):
        #return super().__init__(**kwargs)
        annotations = type_safe_cache.get_obj_annotations(self)
        node_data = kwargs.get('node_data') or annotations.get('node_data')()       # todo: see if need to check if annotations.get('node_data') is a type
        node_id   = kwargs.get('node_id'  ) or Node_Id(Obj_Id())
        node_type = kwargs.get('node_type') or self.__class__
        node_dict = dict(node_data = node_data,
                         node_id   = node_id  ,
                         node_type = node_type)
        object.__setattr__(self, '__dict__', node_dict)



