from unittest                                                                         import TestCase
from osbot_utils.utils.Objects                                                        import base_classes
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label    import Safe_Str__Label
from mgraph_db.mgraph.actions.exporters.plantuml.models.safe_str.Safe_Str__PlantUML   import Safe_Str__PlantUML
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
from mgraph_db.mgraph.utils.MGraph__Static__Graph                                     import MGraph__Static__Graph
from mgraph_db.providers.simple.MGraph__Simple                                        import MGraph__Simple


class test_MGraph__Export__PlantUML(TestCase):

    def setUp(self):
        self.mgraph_simple = MGraph__Simple()

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
        mgraph_data = self.mgraph_simple.data()

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data) as _:
            result = _.render()
            assert type(result)             is Safe_Str__PlantUML                     # returns Safe_Str__PlantUML
            assert '@startuml'              in result                                 # starts correctly
            assert '@enduml'                in result                                 # ends correctly
            assert result == """@startuml
skinparam backgroundColor transparent
skinparam shadowing false


@enduml"""

    def test_render__output_structure(self):                                          # test output structure
        mgraph_data = self.mgraph_simple.data()

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data) as _:
            result = str(_.render())
            lines  = result.split('\n')
            assert lines[0]                 == '@startuml'                            # first line
            assert lines[-1]                == '@enduml'                              # last line
            assert 'skinparam'              in result                                 # has skin params
            assert result == """@startuml
skinparam backgroundColor transparent
skinparam shadowing false


@enduml"""

    def test_render__with_direction(self):                                            # test direction in output
        mgraph_data = self.mgraph_simple.data()
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph(direction='LR')                      ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data, config=config) as _:
            result = _.render()
            assert 'left to right direction' in result
            assert result == """@startuml
skinparam backgroundColor transparent
skinparam shadowing false
left to right direction


@enduml"""

    def test_render__with_title(self):                                                # test title in output
        mgraph_data = self.mgraph_simple.data()
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph(title=Safe_Str__Label('My Graph'))   ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data, config=config) as _:
            result = _.render()
            assert 'title My Graph'         in result

    def test_render__with_nodes(self):                                                # test node rendering
        with self.mgraph_simple.edit() as edit:
            node1 = edit.new_node()
            node2 = edit.new_node()

        mgraph_data = self.mgraph_simple.data()

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data) as _:
            result = _.render()
            node1_id_safe = str(node1.node_id).replace('-', '_')                      # sanitized node ID
            node2_id_safe = str(node2.node_id).replace('-', '_')
            assert node1_id_safe            in result                                 # first node
            assert node2_id_safe            in result                                 # second node

    def test_render__with_edges(self):                                                # test edge rendering
        with self.mgraph_simple.edit() as edit:
            node_a = edit.new_node()
            node_b = edit.new_node()
            edge1  = edit.new_edge(from_node_id=node_a.node_id, to_node_id=node_b.node_id)

        mgraph_data = self.mgraph_simple.data()

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data) as _:
            result = _.render()
            node_a_id_safe = str(node_a.node_id).replace('-', '_')
            node_b_id_safe = str(node_b.node_id).replace('-', '_')
            assert node_a_id_safe           in result
            assert node_b_id_safe           in result
            assert '-->'                    in result                                 # edge arrow

    def test_render__context_accumulation(self):                                      # test context is populated
        with self.mgraph_simple.edit() as edit:
            node1 = edit.new_node()
            node2 = edit.new_node()
            edge1 = edit.new_edge(from_node_id=node1.node_id, to_node_id=node2.node_id)

        mgraph_data = self.mgraph_simple.data()

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data) as _:
            _.render()
            assert len(_.context.nodes)     == 2                                      # 2 nodes rendered
            assert len(_.context.edges)     == 1                                      # 1 edge rendered

    def test_on_add_node__callback(self):                                             # test node callback
        with self.mgraph_simple.edit() as edit:
            node1 = edit.new_node()

        mgraph_data = self.mgraph_simple.data()

        def custom_node_renderer(node, node_data):                                    # custom renderer
            return 'actor "Custom" as custom_node #Yellow'

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data) as _:
            _.on_add_node = custom_node_renderer
            result = _.render()
            assert 'actor "Custom"'         in result                                 # custom output
            assert '#Yellow'                in result

    def test_on_add_node__callback_returns_none(self):                                # test callback returning None
        with self.mgraph_simple.edit() as edit:
            node1 = edit.new_node()

        mgraph_data = self.mgraph_simple.data()

        def passthrough_callback(node, node_data):                                    # returns None = use default
            return None

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data) as _:
            _.on_add_node = passthrough_callback
            result = _.render()
            node1_id_safe = str(node1.node_id).replace('-', '_')
            assert node1_id_safe            in result                                 # default rendering used

    def test_on_add_edge__callback(self):                                             # test edge callback
        with self.mgraph_simple.edit() as edit:
            node_a = edit.new_node()
            node_b = edit.new_node()
            edge1  = edit.new_edge(from_node_id=node_a.node_id, to_node_id=node_b.node_id)

        mgraph_data = self.mgraph_simple.data()

        def custom_edge_renderer(edge, from_node, to_node, edge_data):                # custom renderer
            return 'a ..> b : custom_label'

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data) as _:
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
        mgraph_data = self.mgraph_simple.data()

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data) as _:
            result = (_.set_title('Chained')
                       .left_to_right()
                       .set_node_shape('component')
                       .set_show_node_type(True)
                       .render())

            assert 'title Chained'           in result
            assert 'left to right direction' in result

    # ═══════════════════════════════════════════════════════════════════════════════
    # Integration tests with MGraph__Static__Graph
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__integration__linear_graph(self):                                        # test linear graph rendering
        static_graph = MGraph__Static__Graph.create_linear(num_nodes=3)
        mgraph       = static_graph.graph
        mgraph_data  = mgraph.data()

        with MGraph__Export__PlantUML(graph=mgraph.graph, data=mgraph_data) as _:
            result = _.render()
            assert '@startuml'              in result
            assert '@enduml'                in result
            assert '-->'                    in result                                 # edges present
            assert len(_.context.nodes)     == 3                                      # 3 nodes
            assert len(_.context.edges)     == 2                                      # 2 edges (linear)

    def test__integration__circular_graph(self):                                      # test circular graph rendering
        static_graph = MGraph__Static__Graph.create_circular(num_nodes=4)
        mgraph       = static_graph.graph
        mgraph_data  = mgraph.data()

        with MGraph__Export__PlantUML(graph=mgraph.graph, data=mgraph_data) as _:
            result = _.render()
            assert '@startuml'              in result
            assert '@enduml'                in result
            assert len(_.context.nodes)     == 4                                      # 4 nodes
            assert len(_.context.edges)     == 4                                      # 4 edges (circular)

    def test__integration__star_graph(self):                                          # test star graph rendering
        static_graph = MGraph__Static__Graph.create_star(num_spokes=4)
        mgraph       = static_graph.graph
        mgraph_data  = mgraph.data()

        with MGraph__Export__PlantUML(graph=mgraph.graph, data=mgraph_data) as _:
            result = _.render()
            assert '@startuml'              in result
            assert '@enduml'                in result
            assert len(_.context.nodes)     == 5                                      # 5 nodes (1 center + 4 spokes)
            assert len(_.context.edges)     == 4                                      # 4 edges (to spokes)

    def test__integration__complete_graph(self):                                      # test complete graph rendering
        static_graph = MGraph__Static__Graph.create_complete(num_nodes=4)
        mgraph       = static_graph.graph
        mgraph_data  = mgraph.data()

        with MGraph__Export__PlantUML(graph=mgraph.graph, data=mgraph_data) as _:
            result = _.render()
            assert '@startuml'              in result
            assert '@enduml'                in result
            assert len(_.context.nodes)     == 4                                      # 4 nodes
            assert len(_.context.edges)     == 6                                      # 6 edges (4*3/2 for complete)

    def test__integration__with_title_and_direction(self):                            # test complete graph with config
        static_graph = MGraph__Static__Graph.create_star(num_spokes=3)
        mgraph       = static_graph.graph
        mgraph_data  = mgraph.data()

        with MGraph__Export__PlantUML(graph=mgraph.graph, data=mgraph_data) as _:
            result = (_.set_title('Star Graph')
                       .left_to_right()
                       .render())

            assert '@startuml'              in result
            assert '@enduml'                in result
            assert 'title Star Graph'       in result
            assert 'left to right direction' in result

    def test__integration__output_is_valid_plantuml(self):                            # verify PlantUML syntax
        static_graph = MGraph__Static__Graph.create_linear(num_nodes=2)
        mgraph       = static_graph.graph
        mgraph_data  = mgraph.data()

        with MGraph__Export__PlantUML(graph=mgraph.graph, data=mgraph_data) as _:
            result = str(_.render())
            lines  = [l.strip() for l in result.split('\n') if l.strip()]

            assert lines[0]                 == '@startuml'                            # must start with @startuml
            assert lines[-1]                == '@enduml'                              # must end with @enduml

    def test__integration__with_simple_graph(self):                                   # test with MGraph__Simple
        with self.mgraph_simple.edit() as edit:
            node1 = edit.new_node()
            node2 = edit.new_node()
            node3 = edit.new_node()
            edit.new_edge(from_node_id=node1.node_id, to_node_id=node2.node_id)
            edit.new_edge(from_node_id=node2.node_id, to_node_id=node3.node_id)

        mgraph_data = self.mgraph_simple.data()

        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph, data=mgraph_data) as _:
            result = (_.set_title('Simple Graph')
                       .left_to_right()
                       .render())

            assert '@startuml'              in result
            assert '@enduml'                in result
            assert 'title Simple Graph'     in result
            assert 'left to right direction' in result
            assert '-->'                    in result
            assert len(_.context.nodes)     == 3
            assert len(_.context.edges)     == 2

    def test_process_graph(self):
        with MGraph__Export__PlantUML(graph=self.mgraph_simple.graph) as _:
            plantuml_code = _.render()

            assert  plantuml_code      == """@startuml
skinparam backgroundColor transparent
skinparam shadowing false


@enduml"""
            assert type(plantuml_code) is Safe_Str__PlantUML
