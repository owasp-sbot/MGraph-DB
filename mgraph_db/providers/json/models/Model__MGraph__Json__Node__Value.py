from typing                                                             import Any
from mgraph_db.providers.json.models.Model__MGraph__Json__Node          import Model__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value import Schema__MGraph__Json__Node__Value
from osbot_utils.type_safe.type_safe_core.methods.type_safe_property    import set_as_property

class Model__MGraph__Json__Node__Value(Model__MGraph__Json__Node):                         # Model class for JSON value nodes
    data       : Schema__MGraph__Json__Node__Value
    value_type = set_as_property('data.node_data', 'value_type')

    def __init__(self, **kwargs):
        data      = kwargs.get('data') or self.__annotations__['data']()
        node_dict = dict(data=data)
        object.__setattr__(self, '__dict__', node_dict)

    def is_primitive(self) -> bool:                                                         # Check if the value is a primitive type
        return self.value_type in (str, int, float, bool, type(None))

    @property
    def value(self) -> Any:
        return self.data.node_data.value

    @value.setter
    def value(self, new_value: Any) -> None:
        self.data.node_data.value      = new_value
        self.data.node_data.value_type = type(new_value)