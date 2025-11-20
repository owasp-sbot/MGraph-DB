from mgraph_db.providers.json.models.Model__MGraph__Json__Node             import Model__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property import Schema__MGraph__Json__Node__Property
from osbot_utils.type_safe.type_safe_core.methods.type_safe_property       import set_as_property


class Model__MGraph__Json__Node__Property(Model__MGraph__Json__Node):                      # Model class for JSON object property nodes
    data: Schema__MGraph__Json__Node__Property

    name = set_as_property('data.node_data', 'name')

    def __init__(self, **kwargs):
        data      = kwargs.get('data') or self.__annotations__['data']()
        node_dict = dict(data=data)
        object.__setattr__(self, '__dict__', node_dict)