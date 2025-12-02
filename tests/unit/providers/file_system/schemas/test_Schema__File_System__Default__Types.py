from unittest                                                                    import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                               import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                         import Schema__MGraph__Node__Data
from mgraph_db.providers.file_system.schemas.Schema__File_System__Types          import Schema__File_System__Types
from mgraph_db.providers.file_system.schemas.Schema__File_System__Graph__Config  import Schema__File_System__Graph__Config
from mgraph_db.providers.file_system.schemas.Schema__Folder__Node                import Schema__Folder__Node
from osbot_utils.testing.__                                                      import __

class test_Schema__Types(TestCase):

    def test__init__(self):
        with Schema__File_System__Types() as _:
            assert _.obj() == __(graph_data_type  = 'mgraph_db.providers.file_system.schemas.Schema__File_System__Graph__Config.Schema__File_System__Graph__Config' ,
                                 node_type        = 'mgraph_db.providers.file_system.schemas.Schema__Folder__Node.Schema__Folder__Node'                             ,
                                 edge_type        = None                                            ,
                                 node_data_type   = 'mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data'                                )

            assert _.graph_data_type   is Schema__File_System__Graph__Config
            assert _.node_type         is Schema__Folder__Node
            assert _.edge_type         is None
            assert _.node_data_type    is Schema__MGraph__Node__Data