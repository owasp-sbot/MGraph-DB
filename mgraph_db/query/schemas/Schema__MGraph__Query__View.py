from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id
from mgraph_db.query.schemas.Schema__MGraph__Query__View__Data   import Schema__MGraph__Query__View__Data
from mgraph_db.query.schemas.View_Id                             import View_Id
from osbot_utils.type_safe.Type_Safe                             import Type_Safe


class Schema__MGraph__Query__View(Type_Safe):
    view_id   : View_Id                                                        # Unique view identifier
    view_data : Schema__MGraph__Query__View__Data                              # View data and metadata

    def __init__(self, **kwargs):
        if kwargs.get('view_id') is None:                           # make sure .node_id is set
            kwargs['view_id'] = View_Id(Obj_Id())                   # we need to use Obj_Id() here because Node_Id() == ''
        super().__init__(**kwargs)
