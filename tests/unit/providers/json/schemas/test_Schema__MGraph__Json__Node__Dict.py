from unittest                                                          import TestCase
from osbot_utils.utils.Objects                                         import full_type_name
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict import Schema__MGraph__Json__Node__Dict
from osbot_utils.testing.__                                            import __


class test_Schema__MGraph__Json__Node__Dict(TestCase):
    def test__init__(self):                                                                         # Test Dict node initialization
        with Schema__MGraph__Json__Node__Dict() as _:
            assert _.obj() == __(node_data  =__()           ,
                                 node_id    = _.node_id     ,
                                 node_type  = full_type_name(Schema__MGraph__Json__Node__Dict))
