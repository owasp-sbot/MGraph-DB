from mgraph_db.mgraph.actions.MGraph__Type__Resolver                        import MGraph__Type__Resolver
from mgraph_db.providers.json.models.Model__MGraph__Json__Node              import Model__MGraph__Json__Node
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__List        import Model__MGraph__Json__Node__List
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Property    import Model__MGraph__Json__Node__Property
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Value       import Model__MGraph__Json__Node__Value
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node            import Schema__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__List      import Schema__MGraph__Json__Node__List
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property  import Schema__MGraph__Json__Node__Property
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value     import Schema__MGraph__Json__Node__Value
from mgraph_db.mgraph.models.Model__MGraph__Graph                           import Model__MGraph__Graph
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Dict        import Model__MGraph__Json__Node__Dict
from mgraph_db.providers.json.models.Model__MGraph__Json__Types             import Model__MGraph__Json__Types
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph           import Schema__MGraph__Json__Graph
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict      import Schema__MGraph__Json__Node__Dict

class Model__MGraph__Json__Graph(Model__MGraph__Graph):
    data       : Schema__MGraph__Json__Graph
    model_types: Model__MGraph__Json__Types
    resolver   : MGraph__Type__Resolver

    def __init__(self, **kwargs):                                                                   # todo: this was originally done (Jan 2025) for performance reasons (not using the Type_Safe __init__()
        data        = kwargs.get('data'       ) or self.__annotations__['data']()                   #       see if that is still the case (lots of optimisations done to that library since)
        model_types = kwargs.get('model_types') or self.__annotations__['model_types']()
        node_dict   = dict(data=data, model_types=model_types, resolver=MGraph__Type__Resolver())
        object.__setattr__(self, '__dict__', node_dict)

    def node(self, node_id):
        node  = self.data.nodes.get(node_id)
        if node:
            if node.node_type is Schema__MGraph__Json__Node:            # todo: add a type resolver so that we don't have to hard code all these mappings here
                return Model__MGraph__Json__Node(data=node)
            elif node.node_type is Schema__MGraph__Json__Node__Dict:
                return Model__MGraph__Json__Node__Dict(data=node)
            elif node.node_type is Schema__MGraph__Json__Node__List:
                return Model__MGraph__Json__Node__List(data=node)
            elif node.node_type is Schema__MGraph__Json__Node__Value:
                return Model__MGraph__Json__Node__Value(data=node)
            elif node.node_type is Schema__MGraph__Json__Node__Property:
                return Model__MGraph__Json__Node__Property(data=node)