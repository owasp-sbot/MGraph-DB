from unittest                                                     import TestCase
from osbot_utils.testing.__helpers                                import obj
from osbot_utils.utils.Objects                                    import type_full_name, base_types
from mgraph_db.providers.simple.schemas.Schema__Simple__Node      import Schema__Simple__Node
from osbot_utils.type_safe.Type_Safe                              import Type_Safe
from osbot_utils.testing.__                                       import __
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Cytoscape import MGraph__Export__Cytoscape
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Base      import MGraph__Export__Base
from mgraph_db.providers.simple.MGraph__Simple                    import MGraph__Simple

class test_MGraph__Export__Viz__Cytoscape(TestCase):

    def setUp(self):                                                                    # Initialize test environment
        self.mgraph_simple = MGraph__Simple()
        self.exporter     = MGraph__Export__Cytoscape(graph=self.mgraph_simple.graph)

    def test_init(self):                                                                # Test initialization and inheritance
        assert type(self.exporter)        is MGraph__Export__Cytoscape
        assert base_types(self.exporter) == [MGraph__Export__Base, Type_Safe, object]   # Check inheritance chain

    def test_create_node_data(self):                                                    # Test node data creation
        with self.mgraph_simple.edit() as edit:
            node = edit.new_node(value='test_value', name='test_name')

        node_data = self.exporter.create_node_data(node)
        assert obj(node_data) == __(data  = __( id    = str(node.node_id)               ,       # Check exact structure using __
                                               type  = node.node.data.node_type.__name__,
                                               label = 'test_name'                      ))

    def test_create_edge_data(self):                                                    # Test edge data creation
        with self.mgraph_simple.edit() as edit:
            node_1 = edit.new_node(value='test1')
            node_2 = edit.new_node(value='test2')
            edge_1 = edit.new_edge(from_node_id = node_1.node_id,
                                   to_node_id   = node_2.node_id)

        edge_data = self.exporter.create_edge_data(edge_1)
        assert obj(edge_data) == __( data = __( id     = str(edge_1.edge_id       )         ,    # Check exact structure using __
                                                source = str(edge_1.from_node_id())         ,
                                                target = str(edge_1.to_node_id  ())         ,
                                                type   = edge_1.edge.data.edge_type.__name__))

    def test_format_output(self):                                                       # Test output format
        with self.mgraph_simple.edit() as edit:
            node_1 = edit.new_node(value='test1')
            node_2 = edit.new_node(value='test2')
            edge_1 = edit.new_edge(from_node_id = node_1.node_id,
                                   to_node_id   = node_2.node_id)

        output = self.exporter.process_graph()


        assert type(output)             is dict                                         # Check main structure
        assert 'elements'               in output

        assert 'nodes'                 in output['elements']
        assert 'edges'                 in output['elements']

        nodes = output['elements']['nodes']
        edges = output['elements']['edges']

        assert len(nodes)               == 2                                            # Check content size
        assert len(edges)               == 1

        # Check node structure
        node = nodes[0]
        assert 'data'                  in node

        # Check edge structure
        edge = edges[0]
        assert 'data'                  in edge

        node_1_id = node_1.node_id
        node_2_id = node_2.node_id
        edge_1_id = edge_1.edge_id
        assert output == { 'elements': { 'edges'  : [ { 'data' : { 'id'                 : edge_1_id             ,
                                                                   'source'             : node_1_id             ,
                                                                   'target'             : node_2_id             ,
                                                                   'type'               : 'Schema__MGraph__Edge'}}],
                            'nodes'  : [ { 'data': { 'id'               : node_1_id             ,
                                                     'label'            : 'test1'               ,
                                                     'type'             : 'Schema__Simple__Node'}},
                                         { 'data': { 'id'               : node_2_id             ,
                                                     'label'            : 'test2'               ,
                                                     'type'             : 'Schema__Simple__Node'}}]}}



    def test_get_node_label(self):                                                      # Test label generation
        with self.mgraph_simple.edit() as edit:
            node_1 = edit.new_node(name='test_name')                                     # Test with name
            assert node_1.obj().node                    == __( data = __( node_data = __( value = None                   ,
                                                                                          name  = 'test_name')           ,
                                                                          node_id   = node_1.node_id                     ,
                                                                          node_type = type_full_name(Schema__Simple__Node)))
            assert self.exporter.get_node_label(node_1) == 'test_name'

            node_2 = edit.new_node(value='test_value')                               # Test with value but no name
            assert node_2.obj().node                    == __( data = __( node_data = __( value = 'test_value'                   ,
                                                                                          name  = None)           ,
                                                              node_id   = node_2.node_id                     ,
                                                              node_type = type_full_name(Schema__Simple__Node)))
            assert self.exporter.get_node_label(node_2) == 'test_value'

            node3 = edit.new_node(name='test_name', value='test_value')                         # Test with both name and value (name should take precedence)
            assert self.exporter.get_node_label(node3) == 'test_name'

            node4 = edit.new_node()                                                             # Test with neither name nor value
            assert self.exporter.get_node_label(node4) == node4.node.data.node_type.__name__

