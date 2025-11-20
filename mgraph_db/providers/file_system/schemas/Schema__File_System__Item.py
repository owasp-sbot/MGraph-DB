from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now import Timestamp_Now
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                               import Schema__MGraph__Node



class Schema__File_System__Item(Schema__MGraph__Node):
    created_at   : Timestamp_Now
    modified_at  : Timestamp_Now