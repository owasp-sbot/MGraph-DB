from typing                                                         import Dict, Optional
from mgraph_db.query.schemas.Schema__MGraph__Query__View            import Schema__MGraph__Query__View
from mgraph_db.query.schemas.View_Id                                import View_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Schema__MGraph__Query__Views(Type_Safe):
    views          : Dict[View_Id, Schema__MGraph__Query__View]                # Map of all views
    first_view_id  : Optional[View_Id]                                         # First view in history
    current_view_id: Optional[View_Id]                                         # Current active view
