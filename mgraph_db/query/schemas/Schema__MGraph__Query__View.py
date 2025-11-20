from mgraph_db.query.schemas.Schema__MGraph__Query__View__Data   import Schema__MGraph__Query__View__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id
from osbot_utils.type_safe.Type_Safe                             import Type_Safe


class Schema__MGraph__Query__View(Type_Safe):
    view_id   : Obj_Id                                                         # Unique view identifier
    view_data : Schema__MGraph__Query__View__Data                              # View data and metadata
