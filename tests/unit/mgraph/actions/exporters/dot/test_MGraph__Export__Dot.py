from unittest                                                                   import TestCase
from osbot_utils.testing.__ import __, __SKIP__
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                              import Schema__MGraph__Edge
from mgraph_db.providers.simple.schemas.Schema__Simple__Node                    import Schema__Simple__Node
from osbot_utils.utils.Env                                                      import load_dotenv
from mgraph_db.mgraph.actions.exporters.dot.MGraph__Export__Dot                 import MGraph__Export__Dot
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config  import MGraph__Export__Dot__Config
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                              import Domain__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph                               import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                             import Schema__MGraph__Graph
from mgraph_db.providers.simple.MGraph__Simple__Test_Data                       import MGraph__Simple__Test_Data



class test_MGraph__Export__Dot(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.create_screenshot = False
        cls.screenshot_file   = './export-dot.png'

    def setUp(self):                                                                    # Initialize test environment
        self.simple_graph = MGraph__Simple__Test_Data().create()
        self.nodes_ids    = self.simple_graph.nodes_ids()
        self.edges_ids    = self.simple_graph.edges_ids()
        self.domain_graph = self.simple_graph.graph
        self.exporter     = MGraph__Export__Dot(graph=self.domain_graph)               # Create DOT exporter
        self.exporter.config.render.label_show_var_name = True                         # use this default since a good number of the tests below used it

    def tearDown(self):
        if self.create_screenshot:
            load_dotenv()
            with self.simple_graph.screenshot() as _:
                _.save_to(self.screenshot_file).dot_to_png(self.exporter.dot_code)

    def test_init(self):                                                               # Test initialization
        config = MGraph__Export__Dot__Config()
        config.display.node_value = True
        config.display.edge_id = False
        config.node.font.name = "Times"
        config.node.font.size = 12

        exporter = MGraph__Export__Dot(graph=self.domain_graph, config=config)#.set_graph_node()

        assert type(exporter)                          is MGraph__Export__Dot
        assert exporter.graph                          == self.domain_graph
        assert exporter.config.display.node_value      is True
        assert exporter.config.display.edge_id         is False
        assert exporter.config.node.font.name          == "Times"
        assert exporter.config.node.font.size          == 12

        assert exporter.obj() == __(graph            = self.domain_graph.obj()   ,
                                    context          = __( nodes         = __()                         ,
                                                           edges         = __()                         ,
                                                           counters      = __(node=0, edge=0, other=0)) ,
                                    config           = exporter.config.obj()                            ,
                                    dot_code         = None                                             ,
                                    on_add_node      = None                                             ,
                                    on_add_edge      = None                                             ,
                                    resolver         = __SKIP__                                         ,
                                    node_renderer    = exporter.node_renderer   .obj()                  ,
                                    edge_renderer    = exporter.edge_renderer   .obj()                  ,
                                    style_manager    = exporter.style_manager   .obj()                  ,
                                    format_generator = exporter.format_generator.obj()                  )

    def test_create_node_data(self):                                                   # Test node data creation
        node_id = self.nodes_ids[0]                                                    # Get first node (Node 1)
        node_data = self.exporter.create_node_data(self.domain_graph.node(node_id))

        assert node_data['id']    == str(node_id)
        assert node_data['attrs'] == []

        # Test with show_value=True
        self.exporter.config.display.node_value = True
        self.exporter.config.render.label_show_var_name = True
        node_data                               = self.exporter.create_node_data(self.domain_graph.node(node_id))
        assert 'label="node_value=\'A\'"'    in node_data['attrs']

    def test_create_edge_data(self):                                                   # Test edge data creation
        edge_1_id = self.edges_ids[0]
        node_1_id = self.nodes_ids[0]
        node_2_id = self.nodes_ids[1]
        edge_data = self.exporter.create_edge_data(self.domain_graph.edge(edge_1_id))

        assert edge_data['id']     == str(edge_1_id)
        assert edge_data['source'] == str(node_1_id)
        assert edge_data['target'] == str(node_2_id)
        assert edge_data['type']   == 'Schema__MGraph__Edge'

    def test_format_output(self):                                                      # Test DOT output formatting
        self.exporter.show_edge__id()
        self.exporter.process_graph()                                                  # Process graph first
        dot_output = self.exporter.format_output()

        assert 'digraph {'            in dot_output
        assert str(self.nodes_ids[0]) in dot_output
        assert str(self.nodes_ids[1]) in dot_output
        assert str(self.edges_ids[0]) in dot_output
        assert '->'                   in dot_output
        assert '}'                    in dot_output

        expected_output = ('digraph {\n'
                          f'  "{self.nodes_ids[0]}"\n'
                          f'  "{self.nodes_ids[1]}"\n'
                          f'  "{self.nodes_ids[2]}"\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="  edge_id = \'{self.edges_ids[0]}\'"]\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  edge_id = \'{self.edges_ids[1]}\'"]\n'
                          '}')
        assert dot_output == expected_output

    def test_empty_graph(self):                                                        # Test handling of empty graph
        empty_schema = Schema__MGraph__Graph(nodes      = {}                   ,
                                           edges      = {}                   ,
                                           graph_type = Schema__MGraph__Graph)
        empty_model  = Model__MGraph__Graph (data       = empty_schema        )
        empty_domain = Domain__MGraph__Graph(model      = empty_model         )
        empty_export = MGraph__Export__Dot  (graph      = empty_domain        )
        empty_export.process_graph()                                                   # Process graph first

        dot_output = empty_export.format_output()
        assert dot_output == 'digraph {\n}'

    def test_custom_config(self):                                                      # Test custom configuration
        config = MGraph__Export__Dot__Config()
        config.display.node_value = True
        config.display.edge_id = False
        config.node.font.name = "Courier"
        config.node.font.size = 14
        config.graph.rank_sep = 1.2

        exporter = MGraph__Export__Dot(graph=self.domain_graph, config=config)
        exporter.config.render.label_show_var_name = True
        exporter.process_graph()                                                       # Process graph first
        output = exporter.format_output()

        # With show_value=True, should include label attributes
        assert 'label="node_value=\'A\'"' in output                                                   # First node's value

        # With show_edge_ids=False, should not include edge IDs in labels
        for edge_id in self.edges_ids:
            assert f'label="  {edge_id}"' not in output

    def test_on_add_node(self):                                                             # Test node callback functionality
        def custom_node_handler(node, node_view_data):                                              # Custom node styling based on value
            value = node.node_data.value if node.node_data else None
            if value == "A":
                node_view_data['attrs'] = ['shape=diamond', 'style=filled', 'fillcolor=red'   ]
            if value == "B":
                node_view_data['attrs'] = ['shape=box'    , 'style=filled', 'fillcolor=yellow']

        self.exporter.show_edge__id()
        dot_output = self.exporter.process_graph()                                                                      # first check the result without the custom_node_handler
        expected_output = ('digraph {\n'
                          f'  "{self.nodes_ids[0]}"\n'
                          f'  "{self.nodes_ids[1]}"\n'
                          f'  "{self.nodes_ids[2]}"\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="  edge_id = \'{self.edges_ids[0]}\'"]\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  edge_id = \'{self.edges_ids[1]}\'"]\n'
                          '}')
        assert dot_output == expected_output

        self.exporter.on_add_node = custom_node_handler                                    # Set the callback
        dot_output                = self.exporter.process_graph()
        expected_output = ('digraph {\n'
                          f'  "{self.nodes_ids[0]}" [shape=diamond, style=filled, fillcolor=red]\n'
                          f'  "{self.nodes_ids[1]}" [shape=box, style=filled, fillcolor=yellow]\n'
                          f'  "{self.nodes_ids[2]}"\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="  edge_id = \'{self.edges_ids[0]}\'"]\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  edge_id = \'{self.edges_ids[1]}\'"]\n'
                          '}')
        assert dot_output == expected_output

    def test_on_add_edge(self):                                                             # Test edge callback functionality
        def custom_edge_handler(edge, from_node, to_node, edge_view_data):                               # Custom edge styling based on connected nodes
            if from_node.node_data.value == "A" and to_node.node_data.value == "B":
                edge_view_data['attrs'] = ['color=blue', 'penwidth=2.0', 'label="A to B"']

        self.exporter.show_edge__id()
        dot_output = self.exporter.process_graph()                                          # first check the result without the custom_node_handler
        expected_output = ('digraph {\n'
                          f'  "{self.nodes_ids[0]}"\n'
                          f'  "{self.nodes_ids[1]}"\n'
                          f'  "{self.nodes_ids[2]}"\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="  edge_id = \'{self.edges_ids[0]}\'"]\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  edge_id = \'{self.edges_ids[1]}\'"]\n'
                          '}')
        assert dot_output == expected_output

        self.exporter.on_add_edge = custom_edge_handler                                     # Set the callback
        dot_output = self.exporter.process_graph()                                          # get the updated version of the dot code
        expected_output = ('digraph {\n'
                          f'  "{self.nodes_ids[0]}"\n'
                          f'  "{self.nodes_ids[1]}"\n'
                          f'  "{self.nodes_ids[2]}"\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [color=blue, penwidth=2.0, label="A to B"]\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  edge_id = \'{self.edges_ids[1]}\'"]\n'
                          '}')
        assert dot_output == expected_output

    def test_both_callbacks(self):                                                                  # Test both callbacks together
        def node_handler(node, node_view_data):                                                     # Customize nodes with specific values
            if node.node_data and node.node_data.value in ["A", "B"]:
                node_view_data['attrs'] = [f'label="{node.node_data.value}"', 'shape=circle']

        def edge_handler(edge, from_node, to_node, edge_view_data):                                  # Customize edges between specific nodes
            if all(node.node_data for node in [from_node, to_node]):
                edge_view_data['attrs'] =  [f'label="{from_node.node_data.value} -> {to_node.node_data.value}"']

        self.exporter.show_edge__id()
        self.exporter.on_add_node = node_handler                                         # Set both callbacks
        self.exporter.on_add_edge = edge_handler
        self.exporter.process_graph()                                                    # Process the graph
        dot_output = self.exporter.format_output()

        expected_output = ('digraph {\n'
                          f'  "{self.nodes_ids[0]}" [label="A", shape=circle]\n'
                          f'  "{self.nodes_ids[1]}" [label="B", shape=circle]\n'
                          f'  "{self.nodes_ids[2]}"\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="A -> B"]\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="A -> C"]\n'
                          '}')
        assert dot_output == expected_output
        assert 'label="A"'         in dot_output                                         # Check node customization
        assert 'label="B"'         in dot_output
        assert 'shape=circle'      in dot_output
        assert 'label="A -> B"'    in dot_output                                         # Check edge customization

    def test_edge_source_node_styling(self):                                                 # Test styling of source nodes
        from mgraph_db.mgraph.schemas.Schema__MGraph__Edge import Schema__MGraph__Edge

        self.exporter.set_edge_from_node__type_fill_color(Schema__MGraph__Edge, 'red')
        self.exporter.set_edge_from_node__type_font_color(Schema__MGraph__Edge, 'blue')
        self.exporter.set_edge_from_node__type_font_size(Schema__MGraph__Edge, 14)
        self.exporter.set_edge_from_node__type_shape    (Schema__MGraph__Edge, 'circle')

        dot_output = self.exporter.process_graph()
        assert dot_output == self.exporter.dot_code

        assert dot_output == ('digraph {\n'
                              f'  "{self.nodes_ids[0]}" [fillcolor="red", fontcolor="blue", fontsize="14", shape="circle", style="filled"]\n'
                              f'  "{self.nodes_ids[1]}"\n'
                              f'  "{self.nodes_ids[2]}"\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}"\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}"\n'
                              '}')

    def test_edge_target_node_styling(self):                                                 # Test styling of target nodes
        from mgraph_db.mgraph.schemas.Schema__MGraph__Edge import Schema__MGraph__Edge

        self.exporter.set_edge_to_node__type_fill_color(Schema__MGraph__Edge, 'blue')
        self.exporter.set_edge_to_node__type_font_color(Schema__MGraph__Edge, 'yellow')
        self.exporter.set_edge_to_node__type_font_size (Schema__MGraph__Edge, 14)
        self.exporter.set_edge_to_node__type_shape     (Schema__MGraph__Edge, 'diamond')

        dot_output = self.exporter.process_graph()
        assert dot_output == self.exporter.dot_code

        assert dot_output == ('digraph {\n'
                             f'  "{self.nodes_ids[0]}"\n'
                             f'  "{self.nodes_ids[1]}" [fillcolor="blue", fontcolor="yellow", fontsize="14", shape="diamond", style="filled"]\n'
                             f'  "{self.nodes_ids[2]}" [fillcolor="blue", fontcolor="yellow", fontsize="14", shape="diamond", style="filled"]\n'
                             f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}"\n'
                             f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}"\n'
                             '}')

    def test_edge_mixed_styling(self):                                                       # Test both source and target styling
        from mgraph_db.mgraph.schemas.Schema__MGraph__Edge import Schema__MGraph__Edge

        self.exporter.set_edge_from_node__type_fill_color(Schema__MGraph__Edge, 'red')
        self.exporter.set_edge_from_node__type_shape     (Schema__MGraph__Edge, 'box')
        self.exporter.set_edge_from_node__type_font_size (Schema__MGraph__Edge, 14)
        self.exporter.set_edge_to_node__type_fill_color  (Schema__MGraph__Edge, 'blue')
        self.exporter.set_edge_to_node__type_shape       (Schema__MGraph__Edge, 'diamond')
        self.exporter.set_edge_to_node__type_font_size   (Schema__MGraph__Edge, 16)

        dot_output = self.exporter.process_graph()
        assert dot_output == self.exporter.dot_code

        assert dot_output == ('digraph {\n'
                             f'  "{self.nodes_ids[0]}" [fillcolor="red", fontsize="14", shape="box", style="filled"]\n'
                             f'  "{self.nodes_ids[1]}" [fillcolor="blue", fontsize="16", shape="diamond", style="filled"]\n'
                             f'  "{self.nodes_ids[2]}" [fillcolor="blue", fontsize="16", shape="diamond", style="filled"]\n'
                             f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}"\n'
                             f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}"\n'
                             '}')

    def test_edge_type_style_override(self):                                                # Test style override behavior
        with self.exporter as _:
            _.set_node__type_fill_color          (Schema__Simple__Node, 'green')
            _.set_node__type_shape               (Schema__Simple__Node, 'circle')

            self.exporter.set_edge_from_node__type_fill_color(Schema__MGraph__Edge, 'red')
            self.exporter.set_edge_from_node__type_shape     (Schema__MGraph__Edge, 'box')

            dot_output = _.process_graph()
            assert dot_output == _.dot_code

            assert dot_output == ('digraph {\n'
                                 f'  "{self.nodes_ids[0]}" [fillcolor="red", shape="box", style="filled"]\n'
                                 f'  "{self.nodes_ids[1]}" [fillcolor="green", shape="circle", style="filled"]\n'
                                 f'  "{self.nodes_ids[2]}" [fillcolor="green", shape="circle", style="filled"]\n'
                                 f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}"\n'
                                 f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}"\n'
                                 '}')

    def test_edge_multiple_type_styles(self):                                               # Test styling with multiple edge types
        from mgraph_db.mgraph.schemas.Schema__MGraph__Edge import Schema__MGraph__Edge

        class Custom_Edge_Type(Schema__MGraph__Edge): pass

        self.exporter.set_edge_from_node__type_fill_color(Schema__MGraph__Edge, 'red')
        self.exporter.set_edge_from_node__type_font_size (Schema__MGraph__Edge, 14)
        self.exporter.set_edge_from_node__type_fill_color(Custom_Edge_Type    , 'blue')
        self.exporter.set_edge_from_node__type_font_size (Custom_Edge_Type    , 16)

        dot_output = self.exporter.process_graph()
        assert dot_output == self.exporter.dot_code

        assert dot_output == ('digraph {\n'
                             f'  "{self.nodes_ids[0]}" [fillcolor="red", fontsize="14", style="filled"]\n'
                             f'  "{self.nodes_ids[1]}"\n'
                             f'  "{self.nodes_ids[2]}"\n'
                             f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}"\n'
                             f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}"\n'
                             '}')