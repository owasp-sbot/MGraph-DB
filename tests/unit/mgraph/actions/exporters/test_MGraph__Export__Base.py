from unittest                                                import TestCase
from osbot_utils.testing.__                                  import __
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Base import MGraph__Export__Base, Model__MGraph__Export__Context, Model__MGraph__Export__Context__Counters
from mgraph_db.providers.simple.MGraph__Simple               import MGraph__Simple

class test_MGraph__Export__Base(TestCase):

    def setUp(self):                                                                    # Initialize test environment
        self.mgraph_simple = MGraph__Simple()                                           # Create a simple graph for testing
        self.exporter     = MGraph__Export__Base(graph=self.mgraph_simple.graph)

    def test_init(self):                                                                # Test initialization
        assert type(self.exporter.graph)   == type(self.mgraph_simple.graph)
        assert self.exporter.context.obj() == __(nodes=__(), edges=__(), counters=__(node=0, edge=0, other=0))

    def test_context(self):                                                             # Test context initialization
        context = self.exporter.context
        assert type(context      )      is Model__MGraph__Export__Context               # Check context type
        assert type(context.nodes)      is dict                                         # Check nodes dict
        assert type(context.edges)      is dict                                         # Check edges dict
        assert type(context.counters)   is Model__MGraph__Export__Context__Counters     # Check counters dict
        assert context.counters.node    == 0                                            # Check node counter
        assert context.counters.edge    == 0                                            # Check edge counter

    def test_generate_id(self):                                                # Test ID generation
        id1 = self.exporter.generate_id('node')
        id2 = self.exporter.generate_id('node')
        id3 = self.exporter.generate_id('edge')

        assert id1 == 'node_0'                                                 # Check first node ID
        assert id2 == 'node_1'                                                 # Check second node ID
        assert id3 == 'edge_0'                                                 # Check first edge ID

    def test_process_graph_empty(self):                                        # Test processing empty graph
        result = self.exporter.process_graph()
        assert type(result)                     is dict                        # Check result type
        assert len(result['nodes'])             == 0                          # Check empty nodes
        assert len(result['edges'])             == 0                          # Check empty edges

    def test_process_graph_with_data(self):                                    # Test processing graph with data
        with self.mgraph_simple.edit() as edit:
            node1 = edit.new_node(value='test1')
            node2 = edit.new_node(value='test2')
            edge  = edit.new_edge(from_node_id=node1.node_id,
                                 to_node_id=node2.node_id)

        result = self.exporter.process_graph()
        assert len(result['nodes'])             == 2                          # Check nodes count
        assert len(result['edges'])             == 1                          # Check edges count

        # Check node data structure
        node_data = result['nodes'][0]
        assert 'id'   in node_data
        assert 'type' in node_data

        # Check edge data structure
        edge_data = result['edges'][0]
        assert 'id'     in edge_data
        assert 'source' in edge_data
        assert 'target' in edge_data
        assert 'type'   in edge_data

    def test_create_node_data(self):                                           # Test node data creation
        with self.mgraph_simple.edit() as edit:
            node = edit.new_node(value='test').set_node_type()

        node_data = self.exporter.create_node_data(node)
        assert type(node_data)                  is dict                        # Check return type
        assert str(node.node_id)                == node_data['id']            # Check ID
        assert node.node.data.node_type.__name__ == node_data['type']         # Check type

    def test_create_edge_data(self):                                           # Test edge data creation
        with self.mgraph_simple.edit() as edit:
            node1 = edit.new_node(value='test1')
            node2 = edit.new_node(value='test2')
            edge  = edit.new_edge(from_node_id=node1.node_id,
                                 to_node_id=node2.node_id)

        edge_data = self.exporter.create_edge_data(edge)
        assert type(edge_data)                  is dict                        # Check return type
        assert str(edge.edge_id)                == edge_data['id']            # Check ID
        assert str(edge.from_node_id())         == edge_data['source']        # Check source
        assert str(edge.to_node_id())           == edge_data['target']        # Check target
        assert edge.edge.data.edge_type.__name__ == edge_data['type']         # Check type

    def test_format_output(self):                                              # Test output formatting
        with self.mgraph_simple.edit() as edit:
            node = edit.new_node(value='test')

        self.exporter.process_graph()
        output = self.exporter.format_output()

        assert type(output)                     is dict                        # Check output type
        assert 'nodes' in output                                              # Check nodes presence
        assert 'edges' in output                                              # Check edges presence
        assert type(output['nodes'])            is list                       # Check nodes type
        assert type(output['edges'])            is list                       # Check edges type

    def test_to_dict(self):                                                    # Test dictionary conversion
        with self.mgraph_simple.edit() as edit:
            node1 = edit.new_node(value='test1')
            node2 = edit.new_node(value='test2')
            edge  = edit.new_edge(from_node_id=node1.node_id,
                                 to_node_id=node2.node_id)

        result = self.exporter.to_dict()
        assert type(result)                     is dict                        # Check return type
        assert len(result['nodes'])             == 2                          # Check nodes
        assert len(result['edges'])             == 1                          # Check edges