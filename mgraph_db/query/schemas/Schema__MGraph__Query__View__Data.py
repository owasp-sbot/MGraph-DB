from typing                                                                      import Dict, Set, Optional, Any
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                 import Obj_Id
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now import Timestamp_Now


class Schema__MGraph__Query__View__Data(Type_Safe):
    edges_ids       : Set[Obj_Id]                      # Edge IDs in this view
    next_view_ids   : Set[Obj_Id]
    nodes_ids       : Set[Obj_Id]                      # Node IDs in this view
    previous_view_id: Optional[Obj_Id]                 # Link to previous view
    query_operation : str                              # Type of query operation
    query_params    : Dict[str, Any]                   # Parameters used in query
    timestamp       : Timestamp_Now                    # When view was created

