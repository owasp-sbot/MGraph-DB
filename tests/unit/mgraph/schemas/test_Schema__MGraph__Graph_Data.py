from unittest                                             import TestCase
from osbot_utils.testing.__                               import __
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node        import Schema__MGraph__Node

class Simple_Node(Schema__MGraph__Node): pass               # Helper class for testing

class test__Schema__MGraph__Graph__Data(TestCase):

    def setUp(self):                                        # Initialize test data
        self.graph_data = Schema__MGraph__Graph__Data()

    def test_init(self):                                    # Tests basic initialization and type checking
        assert type(self.graph_data) is Schema__MGraph__Graph__Data
        assert self.graph_data.obj() == __()