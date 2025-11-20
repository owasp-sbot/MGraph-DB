from unittest                                            import TestCase
from osbot_utils.testing.__                              import __
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node       import Schema__MGraph__Node

class Simple_Node(Schema__MGraph__Node): pass                                   # Helper class for testing

class test_Schema__MGraph__Node__Data(TestCase):

    def setUp(self):                                                            # Initialize test data
        self.value_type = str
        self.node_data  = Schema__MGraph__Node__Data()

    def test_init(self):                                                        # Tests basic initialization and type checking
        assert type(self.node_data) is Schema__MGraph__Node__Data
        assert self.node_data.obj() == __()
