from typing                                                         import Dict, Type
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Schema__MGraph__Time_Point__Created__Objects(Type_Safe):                   # The objects that were created

    time_point__node_id : Obj_Id = None                                         # Node IDs created

    timezone__edge_id   : Obj_Id = None
    timezone__node_id   : Obj_Id = None

    utc_offset__edge_id : Obj_Id = None
    utc_offset__node_id : Obj_Id = None

    value_edges__by_type : Dict[Type[Schema__MGraph__Edge], Obj_Id]             # Edge IDs created
    value_nodes__by_type : Dict[Type[Schema__MGraph__Edge], Obj_Id]             # Nodes IDs created