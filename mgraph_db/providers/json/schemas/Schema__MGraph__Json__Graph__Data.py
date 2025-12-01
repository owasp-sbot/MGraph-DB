from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data         import Schema__MGraph__Graph__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id


class Schema__MGraph__Json__Graph__Data(Schema__MGraph__Graph__Data):
    root_id: Node_Id = None                                                     # Store the root node ID


    def __init__(self, **kwargs):
        root_id = kwargs.get('root_id')                     # None default value
        data_dict = dict(root_id = root_id)
        object.__setattr__(self, '__dict__', data_dict)