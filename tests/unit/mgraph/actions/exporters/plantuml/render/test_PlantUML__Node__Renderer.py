from unittest                                                                         import TestCase
from unittest.mock                                                                    import MagicMock, Mock
from osbot_utils.testing.__                                                           import __
from osbot_utils.utils.Objects                                                        import base_classes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id       import Safe_Str__Id

from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                                        import PlantUML__Config
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                                        import PlantUML__Config__Graph
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                                        import PlantUML__Config__Node
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                                        import PlantUML__Config__Edge
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                                        import PlantUML__Config__Display
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Node__Renderer                                import PlantUML__Node__Renderer
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Base                                          import PlantUML__Base


class test_PlantUML__Node__Renderer(TestCase):

    @classmethod
    def setUpClass(cls):                                                              # shared test resources
        cls.config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

    def test__init__(self):                                                           # test auto-initialization
        with PlantUML__Node__Renderer() as _:
            assert type(_)                  is PlantUML__Node__Renderer
            assert PlantUML__Base           in base_classes(_)                        # inherits from base
            assert _.config                 is None
            assert _.graph                  is None
            assert _.index                  is None

    def test__init____with_config(self):                                              # test with config
        with PlantUML__Node__Renderer(config=self.config) as _:
            assert _.config                 is self.config

    def test_render__basic(self):                                                     # test basic node rendering
        node      = self._create_mock_node('node-123', 'Schema__MGraph__Node')
        node_data = None

        with PlantUML__Node__Renderer(config=self.config) as _:
            result = _.render(node, node_data)
            assert 'card'                   in result                                 # default shape
            assert 'node_123'               in result                                 # sanitized ID
            assert '<<Node>>'               in result                                 # type name shown

    def test_render__with_value(self):                                                # test value node rendering
        node      = self._create_mock_node('value-456', 'Schema__MGraph__Node__Value')
        node_data = self._create_mock_node_data('hello world')

        with PlantUML__Node__Renderer(config=self.config) as _:
            result = _.render(node, node_data)
            assert 'hello world'            in result                                 # value shown
            assert 'value_456'              in result                                 # sanitized ID

    def test_render__with_color(self):                                                # test colored node
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(
                        type_colors = {'Node__Value': Safe_Str__Id('LightGreen')}) ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        node      = self._create_mock_node('colored-789', 'Schema__MGraph__Node__Value')
        node_data = self._create_mock_node_data('test')

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(node, node_data)
            assert '#LightGreen'            in result                                 # color applied

    def test_render__shape_rectangle(self):                                           # test rectangle shape
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(shape='rectangle')                    ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        node      = self._create_mock_node('rect-123', 'Schema__MGraph__Node')
        node_data = None

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(node, node_data)
            assert result.startswith('rectangle')                                     # rectangle shape

    def test_render__hide_type(self):                                                 # test hiding type
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_node_type=False)              )

        node      = self._create_mock_node('no-type-123', 'Schema__MGraph__Node')
        node_data = None

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(node, node_data)
            assert '<<'                     not in result                             # type not shown

    def test_render__show_id(self):                                                   # test showing node ID
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_node_id=True)                 )

        node      = self._create_mock_node('id-abc-123', 'Schema__MGraph__Node')
        node_data = None

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(node, node_data)
            assert '[id-abc-1'              in result                                 # truncated ID shown

    def test_build_label__type_only(self):                                            # test label with type only
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_node_type  = True ,
                                                show_node_value = False)           )

        node      = self._create_mock_node('test-123', 'Schema__MGraph__Node')
        node_data = None

        with PlantUML__Node__Renderer(config=config) as _:
            label = _.build_label(node, node_data)
            assert '<<Node>>'               in label

    def test_build_label__value_only(self):                                           # test label with value only
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_node_type  = False,
                                                show_node_value = True )           )

        node      = self._create_mock_node('test-123', 'Schema__MGraph__Node__Value')
        node_data = self._create_mock_node_data('my value')

        with PlantUML__Node__Renderer(config=config) as _:
            label = _.build_label(node, node_data)
            assert 'my value'               in label
            assert '<<'                     not in label                              # no type

    def test_resolve_color__no_mapping(self):                                         # test color without mapping
        with PlantUML__Node__Renderer(config=self.config) as _:
            node = self._create_mock_node('test', 'Schema__MGraph__Node')
            color = _.resolve_color(node)
            assert color                    is None                                   # no default color

    def test_resolve_color__with_default(self):                                       # test default color
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(default_color=Safe_Str__Id('white'))  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with PlantUML__Node__Renderer(config=config) as _:
            node = self._create_mock_node('test', 'Schema__MGraph__Node')
            color = _.resolve_color(node)
            assert color                    == 'white'

    def test_extract_value__with_value(self):                                         # test value extraction
        node_data = self._create_mock_node_data('test value')
        with PlantUML__Node__Renderer(config=self.config) as _:
            value = _.extract_value(node_data)
            assert value                    == 'test value'

    def test_extract_value__none_data(self):                                          # test None node_data
        with PlantUML__Node__Renderer(config=self.config) as _:
            value = _.extract_value(None)
            assert value                    is None

    def test_extract_value__no_value_attr(self):                                      # test data without value
        node_data = Mock()
        del node_data.value                                                           # remove value attr
        with PlantUML__Node__Renderer(config=self.config) as _:
            value = _.extract_value(node_data)
            assert value                    is None

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _create_mock_node(self, node_id: str, type_name: str):                        # create mock node
        node = Mock()
        node.node_id.return_value = node_id

        mock_type = type(type_name, (), {'__name__': type_name})                      # create type with name
        node.node_type.return_value = mock_type
        return node

    def _create_mock_node_data(self, value):                                          # create mock node_data
        node_data = Mock()
        node_data.value = value
        return node_data
