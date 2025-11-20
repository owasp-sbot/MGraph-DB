from unittest                                                   import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge              import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data       import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node              import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data        import Schema__MGraph__Node__Data
from osbot_utils.testing.__                                     import __
from mgraph_db.mgraph.schemas.Schema__MGraph__Types    import Schema__MGraph__Types

class test_Schema__MGraph__Types(TestCase):

    def test__init__(self):
        with Schema__MGraph__Types() as _:
            assert _.obj() == __(edge_type        = 'mgraph_db.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge'                ,
                                 graph_data_type  = 'mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data.Schema__MGraph__Graph__Data'  ,
                                 node_type        = 'mgraph_db.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node'                ,
                                 node_data_type   = 'mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data'    )

            assert _.edge_type        is Schema__MGraph__Edge
            assert _.graph_data_type  is Schema__MGraph__Graph__Data
            assert _.node_type        is Schema__MGraph__Node
            assert _.node_data_type   is Schema__MGraph__Node__Data