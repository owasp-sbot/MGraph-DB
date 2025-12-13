from unittest                                                                         import TestCase
from unittest.mock                                                                    import Mock
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config
from osbot_utils.utils.Objects                                                        import base_classes
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label    import Safe_Str__Label
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Graph
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Node
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Edge
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Display
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Edge__Renderer      import PlantUML__Edge__Renderer
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Base                import PlantUML__Base


class test_PlantUML__Edge__Renderer(TestCase):

    @classmethod
    def setUpClass(cls):                                                              # shared test resources
        cls.config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

    def test__init__(self):                                                           # test auto-initialization
        with PlantUML__Edge__Renderer() as _:
            assert type(_)                  is PlantUML__Edge__Renderer
            assert PlantUML__Base           in base_classes(_)                        # inherits from base
            assert _.config                 is None
            assert _.graph                  is None
            assert _.index                  is None

    def test__init____with_config(self):                                              # test with config
        with PlantUML__Edge__Renderer(config=self.config) as _:
            assert _.config                 is self.config

    def test_render__basic(self):                                                     # test basic edge rendering
        edge      = self._create_mock_edge('edge-123', None)
        from_node = self._create_mock_node('from-node')
        to_node   = self._create_mock_node('to-node')
        edge_data = None

        with PlantUML__Edge__Renderer(config=self.config) as _:
            result = _.render(edge, from_node, to_node, edge_data)
            assert 'from_node'              in result                                 # sanitized from ID
            assert 'to_node'                in result                                 # sanitized to ID
            assert '-->'                    in result                                 # default arrow style

    def test_render__with_predicate(self):                                            # test edge with predicate
        edge      = self._create_mock_edge('edge-456', 'has_property')
        from_node = self._create_mock_node('node-a')
        to_node   = self._create_mock_node('node-b')
        edge_data = None

        with PlantUML__Edge__Renderer(config=self.config) as _:
            result = _.render(edge, from_node, to_node, edge_data)
            assert 'has_property'           in result                                 # predicate shown
            assert ':'                      in result                                 # label separator

    def test_render__custom_arrow_style(self):                                        # test custom arrow
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge(style='..>')                          ,
            display = PlantUML__Config__Display()                                  )

        edge      = self._create_mock_edge('edge-789', None)
        from_node = self._create_mock_node('src')
        to_node   = self._create_mock_node('dst')
        edge_data = None

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(edge, from_node, to_node, edge_data)
            assert '..>'                    in result                                 # custom arrow

    def test_render__hide_predicate(self):                                            # test hiding predicate
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_edge_predicate=False)         )

        edge      = self._create_mock_edge('edge-abc', 'hidden_predicate')
        from_node = self._create_mock_node('a')
        to_node   = self._create_mock_node('b')
        edge_data = None

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(edge, from_node, to_node, edge_data)
            assert 'hidden_predicate'       not in result                             # predicate hidden
            assert ':'                      not in result                             # no label separator

    def test_render__show_edge_type(self):                                            # test showing edge type
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_edge_type=True)               )

        edge      = self._create_mock_edge('edge-type-123', None,
                                           edge_type='Schema__MGraph__Edge__Contains')
        from_node = self._create_mock_node('parent')
        to_node   = self._create_mock_node('child')
        edge_data = None

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(edge, from_node, to_node, edge_data)
            assert '<<'                     in result                                 # type shown with stereotype

    def test_build_label__with_predicate(self):                                       # test label building
        edge = self._create_mock_edge('e1', 'owns')

        with PlantUML__Edge__Renderer(config=self.config) as _:
            label = _.build_label(edge, None)
            assert label                    == 'owns'

    def test_build_label__no_predicate(self):                                         # test label without predicate
        edge = self._create_mock_edge('e1', None)

        with PlantUML__Edge__Renderer(config=self.config) as _:
            label = _.build_label(edge, None)
            assert label                    is None                                   # no label

    def test_build_label__predicate_hidden(self):                                     # test predicate hidden
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_edge_predicate = False,
                                                show_edge_type      = False)       )

        edge = self._create_mock_edge('e1', 'should_be_hidden')

        with PlantUML__Edge__Renderer(config=config) as _:
            label = _.build_label(edge, None)
            assert label                    is None                                   # no label shown

    def test_extract_predicate__with_predicate(self):                                 # test predicate extraction
        edge = self._create_mock_edge('e1', 'has_name')

        with PlantUML__Edge__Renderer(config=self.config) as _:
            predicate = _.extract_predicate(edge)
            assert predicate                == 'has_name'
            assert type(predicate)          is Safe_Str__Label

    def test_extract_predicate__none(self):                                           # test no predicate
        edge = self._create_mock_edge('e1', None)

        with PlantUML__Edge__Renderer(config=self.config) as _:
            predicate = _.extract_predicate(edge)
            assert predicate                is None

    def test_extract_predicate__exception_handling(self):                             # test exception handling
        edge = Mock()
        edge.edge_label.side_effect = Exception('test error')                         # simulate error

        with PlantUML__Edge__Renderer(config=self.config) as _:
            predicate = _.extract_predicate(edge)
            assert predicate                is None                                   # graceful handling

    def test_render__id_sanitization(self):                                           # test ID sanitization in edges
        edge      = self._create_mock_edge('edge-with-special!@#', None)
        from_node = self._create_mock_node('node-with-hyphens')
        to_node   = self._create_mock_node('node with spaces')
        edge_data = None

        with PlantUML__Edge__Renderer(config=self.config) as _:
            result = _.render(edge, from_node, to_node, edge_data)
            assert 'node_with_hyphens'      in result                                 # hyphens sanitized
            assert 'node_with_spaces'       in result                                 # spaces sanitized

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _create_mock_node(self, node_id: str):                                        # create mock node
        node = Mock()
        node.node_id.return_value = node_id
        return node

    def _create_mock_edge(self, edge_id: str, predicate: str,                         # create mock edge
                          edge_type: str = 'Schema__MGraph__Edge'):
        edge = Mock()
        edge.edge_id.return_value = edge_id

        if predicate:                                                                 # set up edge_label
            edge_label       = Mock()
            edge_label.predicate = predicate
            edge.edge_label.return_value = edge_label
        else:
            edge.edge_label.return_value = None

        mock_type = type(edge_type, (), {'__name__': edge_type})                      # create type with name
        edge.edge_type.return_value = mock_type

        return edge
