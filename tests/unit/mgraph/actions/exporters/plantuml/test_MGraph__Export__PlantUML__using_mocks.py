from unittest                                                                         import TestCase
from unittest.mock                                                                    import Mock
from osbot_utils.testing.__                                                           import __
from osbot_utils.utils.Objects                                                        import base_classes
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label    import Safe_Str__Label
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text          import Safe_Str__Text
from mgraph_db.mgraph.actions.exporters.plantuml.MGraph__Export__PlantUML             import MGraph__Export__PlantUML
from mgraph_db.mgraph.actions.exporters.plantuml.MGraph__Export__PlantUML             import PlantUML__Context
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Graph
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Node
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Edge
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Display
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Node__Renderer      import PlantUML__Node__Renderer
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Edge__Renderer      import PlantUML__Edge__Renderer
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Format__Generator   import PlantUML__Format__Generator


class test_MGraph__Export__PlantUML__using_mocks(TestCase):

    def test__init__(self):                                                           # test auto-initialization
        with MGraph__Export__PlantUML() as _:
            assert type(_)                  is MGraph__Export__PlantUML
            assert base_classes(_)          == [Type_Safe, object]
            assert _.graph                  is None
            assert _.index                  is None
            assert _.data                   is None
            assert _.config                 is None
            assert _.context                is None
            assert _.node_renderer          is None
            assert _.edge_renderer          is None
            assert _.format_generator       is None
            assert _.on_add_node            is None                                   # callback not set
            assert _.on_add_edge            is None                                   # callback not set

    def test_setup(self):                                                             # test setup initialization
        with MGraph__Export__PlantUML() as _:
            result = _.setup()
            assert result                   is _                                      # returns self
            assert type(_.config)           is PlantUML__Config                       # config created
            assert type(_.context)          is PlantUML__Context                      # context created
            assert type(_.node_renderer)    is PlantUML__Node__Renderer               # renderer created
            assert type(_.edge_renderer)    is PlantUML__Edge__Renderer               # renderer created
            assert type(_.format_generator) is PlantUML__Format__Generator            # generator created

    def test_setup__preserves_existing_config(self):                                  # test setup doesn't override
        custom_config = PlantUML__Config(
            graph   = PlantUML__Config__Graph(direction='LR')                      ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with MGraph__Export__PlantUML(config=custom_config) as _:
            _.setup()
            assert _.config                 is custom_config                          # original preserved
            assert _.config.graph.direction == 'LR'

    def test_render__empty_graph(self):                                               # test rendering empty graph
        mock_data = self._create_mock_data([], [])

        with MGraph__Export__PlantUML(data=mock_data) as _:
            result = _.render()
            assert type(result)             is Safe_Str__Text                         # returns Safe_Str__Text
            assert '@startuml'              in result                                 # starts correctly
            assert '@enduml'                in result                                 # ends correctly

    def test_render__output_structure(self):                                          # test output structure
        mock_data = self._create_mock_data([], [])

        with MGraph__Export__PlantUML(data=mock_data) as _:
            result = str(_.render())
            lines  = result.split('\n')
            assert lines[0]                 == '@startuml'                            # first line
            assert lines[-1]                == '@enduml'                              # last line
            assert 'skinparam'              in result                                 # has skin params

    def test_render__with_direction(self):                                            # test direction in output
        mock_data = self._create_mock_data([], [])
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph(direction='LR')                      ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with MGraph__Export__PlantUML(data=mock_data, config=config) as _:
            result = _.render()
            assert 'left to right direction' in result

    def test_render__with_title(self):                                                # test title in output
        mock_data = self._create_mock_data([], [])
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph(title=Safe_Str__Label('My Graph'))   ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with MGraph__Export__PlantUML(data=mock_data, config=config) as _:
            result = _.render()
            assert 'title My Graph'         in result

    def test_render__with_nodes(self):                                                # test node rendering
        node1    = self._create_mock_node('node-1', 'Schema__MGraph__Node')
        node2    = self._create_mock_node('node-2', 'Schema__MGraph__Node__Value', 'hello')
        mock_data = self._create_mock_data([node1, node2], [])

        with MGraph__Export__PlantUML(data=mock_data) as _:
            result = _.render()
            assert 'node_1'                 in result                                 # first node
            assert 'node_2'                 in result                                 # second node

    def test_render__with_edges(self):                                                # test edge rendering
        node1    = self._create_mock_node('node-a', 'Schema__MGraph__Node')
        node2    = self._create_mock_node('node-b', 'Schema__MGraph__Node')
        edge1    = self._create_mock_edge('edge-1', 'node-a', 'node-b', 'has_property')
        mock_data = self._create_mock_data([node1, node2], [edge1])

        with MGraph__Export__PlantUML(data=mock_data) as _:
            result = _.render()
            assert 'node_a'                 in result
            assert 'node_b'                 in result
            assert '-->'                    in result                                 # edge arrow
            assert 'has_property'           in result                                 # predicate

    def test_render__context_accumulation(self):                                      # test context is populated
        node1    = self._create_mock_node('n1', 'Schema__MGraph__Node')
        node2    = self._create_mock_node('n2', 'Schema__MGraph__Node')
        edge1    = self._create_mock_edge('e1', 'n1', 'n2', None)
        mock_data = self._create_mock_data([node1, node2], [edge1])

        with MGraph__Export__PlantUML(data=mock_data) as _:
            _.render()
            assert len(_.context.nodes)     == 2                                      # 2 nodes rendered
            assert len(_.context.edges)     == 1                                      # 1 edge rendered

    def test_on_add_node__callback(self):                                             # test node callback
        node1    = self._create_mock_node('custom-node', 'Schema__MGraph__Node')
        mock_data = self._create_mock_data([node1], [])

        def custom_node_renderer(node, node_data):                                    # custom renderer
            return 'actor "Custom" as custom_node #Yellow'

        with MGraph__Export__PlantUML(data=mock_data) as _:
            _.on_add_node = custom_node_renderer
            result = _.render()
            assert 'actor "Custom"'         in result                                 # custom output
            assert '#Yellow'                in result

    def test_on_add_node__callback_returns_none(self):                                # test callback returning None
        node1    = self._create_mock_node('node-1', 'Schema__MGraph__Node')
        mock_data = self._create_mock_data([node1], [])

        def passthrough_callback(node, node_data):                                    # returns None = use default
            return None

        with MGraph__Export__PlantUML(data=mock_data) as _:
            _.on_add_node = passthrough_callback
            result = _.render()
            assert 'node_1'                 in result                                 # default rendering used

    def test_on_add_edge__callback(self):                                             # test edge callback
        node1    = self._create_mock_node('a', 'Schema__MGraph__Node')
        node2    = self._create_mock_node('b', 'Schema__MGraph__Node')
        edge1    = self._create_mock_edge('e1', 'a', 'b', None)
        mock_data = self._create_mock_data([node1, node2], [edge1])

        def custom_edge_renderer(edge, from_node, to_node, edge_data):                # custom renderer
            return 'a ..> b : custom_label'

        with MGraph__Export__PlantUML(data=mock_data) as _:
            _.on_add_edge = custom_edge_renderer
            result = _.render()
            assert '..>'                    in result                                 # custom arrow
            assert 'custom_label'           in result                                 # custom label

    def test_set_direction(self):                                                     # test fluent direction setter
        with MGraph__Export__PlantUML() as _:
            result = _.set_direction('LR')
            assert result                   is _                                      # returns self
            assert _.config.graph.direction == 'LR'

    def test_set_title(self):                                                         # test fluent title setter
        with MGraph__Export__PlantUML() as _:
            result = _.set_title('Test Title')
            assert result                   is _                                      # returns self
            assert _.config.graph.title     == 'Test Title'

    def test_set_node_shape(self):                                                    # test fluent shape setter
        with MGraph__Export__PlantUML() as _:
            result = _.set_node_shape('rectangle')
            assert result                   is _                                      # returns self
            assert _.config.node.shape      == 'rectangle'

    def test_set_show_node_type(self):                                                # test fluent display setter
        with MGraph__Export__PlantUML() as _:
            _.set_show_node_type(False)
            assert _.config.display.show_node_type == False

    def test_set_show_node_value(self):                                               # test fluent display setter
        with MGraph__Export__PlantUML() as _:
            _.set_show_node_value(False)
            assert _.config.display.show_node_value == False

    def test_set_show_edge_predicate(self):                                           # test fluent display setter
        with MGraph__Export__PlantUML() as _:
            _.set_show_edge_predicate(False)
            assert _.config.display.show_edge_predicate == False

    def test_left_to_right(self):                                                     # test convenience method
        with MGraph__Export__PlantUML() as _:
            result = _.left_to_right()
            assert result                   is _
            assert _.config.graph.direction == 'LR'

    def test_top_to_bottom(self):                                                     # test convenience method
        with MGraph__Export__PlantUML() as _:
            result = _.top_to_bottom()
            assert result                   is _
            assert _.config.graph.direction == 'TB'

    def test_fluent_chaining(self):                                                   # test method chaining
        mock_data = self._create_mock_data([], [])

        with MGraph__Export__PlantUML(data=mock_data) as _:
            result = (_.set_title('Chained')
                       .left_to_right()
                       .set_node_shape('component')
                       .set_show_node_type(True)
                       .render())

            assert 'title Chained'           in result
            assert 'left to right direction' in result

    # ═══════════════════════════════════════════════════════════════════════════════
    # Integration tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__integration__complete_graph(self):                                      # test complete graph rendering
        node1    = self._create_mock_node('person-1', 'Schema__MGraph__Node', 'Alice')
        node2    = self._create_mock_node('city-1', 'Schema__MGraph__Node', 'London')
        edge1    = self._create_mock_edge('e1', 'person-1', 'city-1', 'lives_in')
        mock_data = self._create_mock_data([node1, node2], [edge1])

        with MGraph__Export__PlantUML(data=mock_data) as _:
            result = (_.set_title('People and Cities')
                       .left_to_right()
                       .render())

            assert '@startuml'              in result
            assert '@enduml'                in result
            assert 'title People and Cities' in result
            assert 'left to right direction' in result
            assert 'person_1'               in result
            assert 'city_1'                 in result
            assert 'lives_in'               in result

    def test__integration__output_is_valid_plantuml(self):                            # verify PlantUML syntax
        node1    = self._create_mock_node('n1', 'Schema__MGraph__Node')
        mock_data = self._create_mock_data([node1], [])

        with MGraph__Export__PlantUML(data=mock_data) as _:
            result = str(_.render())
            lines  = [l.strip() for l in result.split('\n') if l.strip()]

            assert lines[0]                 == '@startuml'                            # must start with @startuml
            assert lines[-1]                == '@enduml'                              # must end with @enduml

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _create_mock_data(self, nodes, edges):                                        # create mock MGraph__Data
        mock_data = Mock()

        node_dict = {n.node_id(): n for n in nodes}                                   # build node lookup
        edge_dict = {e.edge_id(): e for e in edges}

        mock_data.nodes_ids.return_value = list(node_dict.keys())
        mock_data.edges_ids.return_value = list(edge_dict.keys())
        mock_data.node.side_effect       = lambda nid: node_dict.get(nid)
        mock_data.edge.side_effect       = lambda eid: edge_dict.get(eid)

        return mock_data

    def _create_mock_node(self, node_id: str, type_name: str, value: str = None):     # create mock node
        node = Mock()
        node.node_id.return_value = node_id

        mock_type = type(type_name, (), {'__name__': type_name})
        node.node_type.return_value = mock_type

        if value:                                                                     # set up node_data with value
            node_data       = Mock()
            node_data.value = value
            node.node_data.return_value = node_data
        else:
            node.node_data.return_value = None

        return node

    def _create_mock_edge(self, edge_id: str, from_id: str, to_id: str, predicate: str):  # create mock edge
        edge = Mock()
        edge.edge_id.return_value       = edge_id
        edge.from_node_id.return_value  = from_id
        edge.to_node_id.return_value    = to_id

        if predicate:
            edge_label = Mock()
            edge_label.predicate = predicate
            edge.edge_label.return_value = edge_label
        else:
            edge.edge_label.return_value = None

        edge.edge_data.return_value = None

        mock_type = type('Schema__MGraph__Edge', (), {'__name__': 'Schema__MGraph__Edge'})
        edge.edge_type.return_value = mock_type

        return edge
