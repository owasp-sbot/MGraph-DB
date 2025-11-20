import unittest

from osbot_utils.utils.Objects                                          import full_type_name
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__List  import Schema__MGraph__Json__Node__List
from osbot_utils.testing.__                                             import __


class test_Schema__MGraph__Json__Node__List(unittest.TestCase):
    def test__init__(self):                                                                         # Test List node initialization
        with Schema__MGraph__Json__Node__List() as _:
            assert _.obj() == __(node_data  =__(),
                                 node_type  = full_type_name(Schema__MGraph__Json__Node__List),
                                 node_id    = _.node_id)
