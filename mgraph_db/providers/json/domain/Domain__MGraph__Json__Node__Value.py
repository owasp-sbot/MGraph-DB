from osbot_utils.type_safe.type_safe_core.methods.type_safe_property    import set_as_property
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Value   import Model__MGraph__Json__Node__Value
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node         import Domain__MGraph__Json__Node


class Domain__MGraph__Json__Node__Value(Domain__MGraph__Json__Node):
    node: Model__MGraph__Json__Node__Value                                                         # Reference to value node model

    value      = set_as_property('node', 'value'     )                                             # Value property
    value_type = set_as_property('node', 'value_type')                                             # Value type property

    # def __init__(self, **kwargs):
    #     annotations = type_safe_cache.get_obj_annotations(self)
    #     node        = kwargs.get('node'      ) or annotations['node']()
    #     graph       = kwargs.get('graph'     ) or annotations['graph']()
    #
    #     #value       = kwargs.get('value'     ) or self.value
    #     #value_type  = kwargs.get('value_type') or self.value_type
    #     node_dict   = dict(node  = node  ,
    #                        graph = graph ,
    #                        #value = value ,
    #                        #value_type = value_type
    #                        )
    #
    #     object.__setattr__(self, '__dict__', node_dict)

    def is_primitive(self) -> bool:                                                                # Check if value is a JSON primitive
        return self.node.is_primitive()