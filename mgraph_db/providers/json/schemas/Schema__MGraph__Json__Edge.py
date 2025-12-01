from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Cache   import type_safe_cache
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge

class Schema__MGraph__Json__Edge(Schema__MGraph__Edge):

    def __init__(self, **kwargs):

        self.__annotations__ = type_safe_cache.get_obj_annotations(self)            # need to do this because there some cases where the __annotations__ was being lost when using from_json

        edge_data    = kwargs.get('edge_data'   ) or self.__annotations__['edge_data'  ]()
        edge_type    = kwargs.get('edge_type'   ) or self.__class__
        edge_id      = kwargs.get('edge_id'     ) or Edge_Id(Obj_Id())
        from_node_id = kwargs.get('from_node_id') or Node_Id(Obj_Id())
        to_node_id   = kwargs.get('to_node_id'  ) or Node_Id(Obj_Id())


        edge_dict = dict(edge_data    = edge_data   ,
                         edge_type    = edge_type   ,
                         edge_id      = edge_id     ,
                         from_node_id = from_node_id,
                         to_node_id   = to_node_id  )

        object.__setattr__(self, '__dict__', edge_dict)