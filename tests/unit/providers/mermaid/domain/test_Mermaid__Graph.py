from unittest                                                   import TestCase
from osbot_utils.utils.Objects                                  import __, type_full_name
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Graph  import Domain__Mermaid__Graph

class test_Mermaid__MGraph(TestCase):

    def setUp(self):
        self.mermaid_graph = Domain__Mermaid__Graph()

    def test__init__(self):
        with self.mermaid_graph as _:
            graph_id = _.graph_id()
            assert type(_) is Domain__Mermaid__Graph
            assert _.obj() == __(domain_types  = __(node_domain_type='mgraph_db.providers.mermaid.domain.Domain__Mermaid__Node.Domain__Mermaid__Node',
                                                     edge_domain_type='mgraph_db.providers.mermaid.domain.Domain__Mermaid__Edge.Domain__Mermaid__Edge'),
                                 graph_type    = type_full_name(Domain__Mermaid__Graph)                                                                ,
                                 model         = __(data=__(schema_types = __(edge_type         = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge.Schema__Mermaid__Edge'                    ,
                                                                              edge_config_type  = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge__Config.Schema__Mermaid__Edge__Config'    ,
                                                                              graph_data_type = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph__Config.Schema__Mermaid__Graph__Config'  ,
                                                                              node_type         = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node'                    ,
                                                                              node_data_type  = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data.Schema__Mermaid__Node__Data'          ),
                                                            edges        = __(),
                                                            graph_data   = __(allow_circle_edges    = False,
                                                                              allow_duplicate_edges = False,
                                                                              graph_title           = ''   ),
                                                            graph_id      = graph_id ,
                                                            graph_type    = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph.Schema__Mermaid__Graph',
                                                            mermaid_code  = [],
                                                            nodes         =__(),
                                                            render_config = __(add_nodes         = True   ,
                                                                                                 diagram_direction = 'LR'   ,
                                                                                                 diagram_type      = 'graph',
                                                                                                 line_before_edges = True   ,
                                                                                                 directives        = []     )),
                                                    model_types=__(node_model_type='mgraph_db.providers.mermaid.models.Model__Mermaid__Node.Model__Mermaid__Node',
                                                                     edge_model_type='mgraph_db.providers.mermaid.models.Model__Mermaid__Edge.Model__Mermaid__Edge')))
