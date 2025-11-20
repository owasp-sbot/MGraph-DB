from typing                                                         import Dict, Optional
from mgraph_db.query.schemas.Schema__MGraph__Query__View            import Schema__MGraph__Query__View
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Schema__MGraph__Query__Views(Type_Safe):
    views          : Dict[Obj_Id, Schema__MGraph__Query__View]                # Map of all views
    first_view_id  : Optional[Obj_Id]                                         # First view in history
    current_view_id: Optional[Obj_Id]                                         # Current active view
