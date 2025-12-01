from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                     import Schema__MGraph__Graph
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph__Data import Schema__MGraph__Json__Graph__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Types       import Schema__MGraph__Json__Types
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id      import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id        import Obj_Id


class Schema__MGraph__Json__Graph(Schema__MGraph__Graph):
    schema_types : Schema__MGraph__Json__Types
    graph_data   : Schema__MGraph__Json__Graph__Data

    def __init__(self, **kwargs):
        graph_data    = kwargs.get('graph_data'   ) or self.__annotations__['graph_data']()
        graph_id      = kwargs.get('graph_id'     ) or Graph_Id(Obj_Id())
        graph_type    = kwargs.get('graph_type'   ) or self.__class__
        schema_types  = kwargs.get('schema_types' ) or self.__annotations__['schema_types']()
        edges         = kwargs.get('edges'        ) or {}
        nodes         = kwargs.get('nodes'        ) or {}

        graph_dict = dict(graph_data   = graph_data   ,
                          graph_id     = graph_id     ,
                          graph_type   = graph_type   ,
                          schema_types = schema_types ,
                          edges        = edges        ,
                          nodes        = nodes        )
        object.__setattr__(self, '__dict__', graph_dict)