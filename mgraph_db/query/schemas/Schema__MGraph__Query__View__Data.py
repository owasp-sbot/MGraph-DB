from typing                                                                      import Dict, Set, Optional, Any
from mgraph_db.query.schemas.View_Id                                             import View_Id
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now import Timestamp_Now


class Schema__MGraph__Query__View__Data(Type_Safe):
    edges_ids       : Set[Edge_Id]                      # Edge IDs in this view
    next_view_ids   : Set[View_Id]
    nodes_ids       : Set[Node_Id]                      # Node IDs in this view
    previous_view_id: Optional[View_Id]                 # Link to previous view
    query_operation : str                               # Type of query operation
    query_params    : Dict[str, Any]                    # Parameters used in query          # todo: change to use Type_Safe Primitives
    timestamp       : Timestamp_Now                     # When view was created

