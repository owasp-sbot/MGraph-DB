from unittest                                          import TestCase
from osbot_utils.testing.__                            import __
from mgraph_db.mgraph.schemas.Schema__MGraph__Types    import Schema__MGraph__Types

class test_Schema__MGraph__Types(TestCase):

    def test__init__(self):
        with Schema__MGraph__Types() as _:
            assert _.obj() == __(edge_type=None,
                                 graph_data_type=None,
                                 node_type=None,
                                 node_data_type=None)

            # assert _.edge_type        is Schema__MGraph__Edge
            # assert _.graph_data_type  is Schema__MGraph__Graph__Data
            # assert _.node_type        is Schema__MGraph__Node
            # assert _.node_data_type   is Schema__MGraph__Node__Data