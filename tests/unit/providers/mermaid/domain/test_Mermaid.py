from unittest                                                       import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import is_obj_id
from osbot_utils.utils.Objects                                      import full_type_name
from mgraph_db.mgraph.actions.MGraph__Edit                          import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Screenshot                    import MGraph__Screenshot
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Graph      import Domain__Mermaid__Graph
from mgraph_db.query.MGraph__Query                                  import MGraph__Query
from osbot_utils.testing.__ import __, __SKIP__
from mgraph_db.providers.mermaid.MGraph__Mermaid                    import MGraph__Mermaid


class test_Mermaid(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mermaid = MGraph__Mermaid(graph_id='050670e7')

    def test__init__(self):
        with self.mermaid as _:
            graph_id = _.data().graph_id()
            assert type(_) is MGraph__Mermaid
            assert is_obj_id(graph_id) is True
            assert _.obj()             == __(graph=__(domain_types=__(node_domain_type='mgraph_db.providers.mermaid.domain.Domain__Mermaid__Node.Domain__Mermaid__Node',
                                                                    edge_domain_type='mgraph_db.providers.mermaid.domain.Domain__Mermaid__Edge.Domain__Mermaid__Edge'),
                                                    model=__(data=__(edges=__(),
                                                                     graph_data=__(allow_circle_edges=False,
                                                                                   allow_duplicate_edges=False,
                                                                                   graph_title=''),
                                                                     graph_id='050670e7',
                                                                     graph_type='mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph.Schema__Mermaid__Graph',
                                                                     nodes=__(),
                                                                     schema_types=__(edge_type='mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge.Schema__Mermaid__Edge',
                                                                                     graph_data_type='mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph__Config.Schema__Mermaid__Graph__Config',
                                                                                     node_type='mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node',
                                                                                     node_data_type='mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data.Schema__Mermaid__Node__Data',
                                                                                     edge_config_type='mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge__Config.Schema__Mermaid__Edge__Config'),
                                                                     mermaid_code=[],
                                                                     render_config=__(add_nodes=True,
                                                                                      diagram_direction='LR',
                                                                                      diagram_type='graph',
                                                                                      line_before_edges=True,
                                                                                      directives=[]),
                                                                     graph_path=None),
                                                             model_types=__(node_model_type='mgraph_db.providers.mermaid.models.Model__Mermaid__Node.Model__Mermaid__Node',
                                                                            edge_model_type='mgraph_db.providers.mermaid.models.Model__Mermaid__Edge.Model__Mermaid__Edge'),
                                                             resolver=__SKIP__),
                                                    resolver=__SKIP__,
                                                    graph_type=None),
                                           query_class='mgraph_db.query.MGraph__Query.MGraph__Query',
                                           edit_class='mgraph_db.mgraph.actions.MGraph__Edit.MGraph__Edit',
                                           screenshot_class='mgraph_db.mgraph.actions.MGraph__Screenshot.MGraph__Screenshot')


            # assert _.obj()             == __(graph=__(domain_types   = __(node_domain_type='mgraph_db.providers.mermaid.domain.Domain__Mermaid__Node.Domain__Mermaid__Node',
            #                                                              edge_domain_type='mgraph_db.providers.mermaid.domain.Domain__Mermaid__Edge.Domain__Mermaid__Edge'),
            #                                           graph_type    = full_type_name(Domain__Mermaid__Graph)                                                               ,
            #                                           model         = __(data=__(schema_types  = __(edge_type         = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge.Schema__Mermaid__Edge'                  ,
            #                                                                                         edge_config_type  = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge__Config.Schema__Mermaid__Edge__Config'  ,
            #                                                                                         graph_data_type   = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph__Config.Schema__Mermaid__Graph__Config',
            #                                                                                         node_type         = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node'                  ,
            #                                                                                         node_data_type  = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data.Schema__Mermaid__Node__Data'  ),
            #                                                                      edges        = __(),
            #                                                                      graph_data   = __(allow_circle_edges    = False,
            #                                                                                        allow_duplicate_edges = False,
            #                                                                                        graph_title           = ''   ),
            #                                                                      graph_id     = graph_id                         ,
            #                                                                      graph_type   = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph.Schema__Mermaid__Graph',
            #                                                                      mermaid_code = [],
            #                                                                      nodes        = __(),
            #                                                                      render_config=__(add_nodes         = True   ,
            #                                                                                       diagram_direction = 'LR'   ,
            #                                                                                       diagram_type      = 'graph',
            #                                                                                       line_before_edges = True   ,
            #                                                                                       directives        = []     )),
            #                                                              model_types =__(node_model_type='mgraph_db.providers.mermaid.models.Model__Mermaid__Node.Model__Mermaid__Node',
            #                                                                               edge_model_type='mgraph_db.providers.mermaid.models.Model__Mermaid__Edge.Model__Mermaid__Edge'))),
            #                                  query_class      = full_type_name(MGraph__Query     ),
            #                                  edit_class       = full_type_name(MGraph__Edit      ),
            #                                  screenshot_class = full_type_name(MGraph__Screenshot))
