from unittest                                            import TestCase



class test_README_examples(TestCase):

    def test_1__add_two_nodes_and_one_edge(self):                                               # Test creating and connecting two nodes with an edge

        from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id                   # Required for object ID handling
        from mgraph_db.mgraph.MGraph                                        import MGraph                   # Core MGraph functionality
        from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node     # Node domain class
        from mgraph_db.mgraph.domain.Domain__MGraph__Edge                   import Domain__MGraph__Edge     # Edge domain class

        mgraph = MGraph()                                                                       # Create a new graph instance

        with mgraph.edit() as edit:                                                             # Use edit context for graph modifications
            node_1 = edit.new_node(value="First Node")                                          # Create first node with value
            node_2 = edit.new_node(value="Second Node")                                         # Create second node with value

            edge_1 = edit.new_edge(from_node_id = node_1.node_id,                               # Create edge connecting the nodes
                                   to_node_id   = node_2.node_id)                               # Using their node IDs

            assert node_1 is not None                                                           # Verify first node was created
            assert node_2 is not None                                                           # Verify second node was created
            assert edge_1 is not None                                                           # Verify edge was created

            assert type(node_1) is Domain__MGraph__Node                                         # Verify first node has correct type
            assert type(node_2) is Domain__MGraph__Node                                         # Verify second node has correct type
            assert type(edge_1) is Domain__MGraph__Edge                                         # Verify edge has correct type

            assert type(node_1.node_id) is Obj_Id                                               # Verify first node ID has correct type
            assert type(node_2.node_id) is Obj_Id                                               # Verify second node ID has correct type
            assert type(edge_1.edge_id) is Obj_Id                                               # Verify edge ID has correct type


        # Query the graph
        with mgraph.data() as data:
            nodes     = data.nodes()
            nodes_ids = data.nodes_ids()
            edges     = data.edges()
            edges_ids = data.edges_ids()

            assert len(nodes) == 2
            assert len(edges) == 1


    # todo: fix texts below
    # def test_genai_integration(self):
    #     """Test GenAI integration example from README"""
    #     mgraph = MGraph()
    #     with mgraph.edit() as edit:
    #         # Create a knowledge graph for LLM context
    #         context  = edit.new_node (node_data   = {"type": "context",
    #                                                  "value": "user query"})
    #         entity  = edit.new_node  (node_data  = { "type": "entity",
    #                                                  "value": "named entity"})
    #         relation = edit.new_edge (from_node_id = context.node_id,
    #                                   to_node_id   = entity.node_id,
    #                                   edge_data    = {"type": "contains"})
    #
    #         # Verify the knowledge graph
    #         assert context.node_data.value == "user query"
    #         assert entity.node_data.value == "named entity"
    #         assert relation.edge_data.type == "contains"
    #
    # def test_semantic_web(self):
    #     """Test Semantic Web example from README"""
    #     mgraph = MGraph()
    #     with mgraph.edit() as edit:
    #         # Create RDF-style triples
    #         subject = edit.new_node(node_data={"uri": "http://example.org/subject"})
    #         object = edit.new_node(node_data={"uri": "http://example.org/object"})
    #         predicate = edit.new_edge(from_node_id=subject.node_id,
    #                                  to_node_id=object.node_id,
    #                                  edge_data={"predicate": "relates_to"})
    #
    #         # Verify triple structure
    #         assert subject.node_data.uri == "http://example.org/subject"
    #         assert object.node_data.uri == "http://example.org/object"
    #         assert predicate.edge_data.predicate == "relates_to"
    #
    # def test_type_safe_operations(self):
    #     """Test type-safe operations example from README"""
    #     # Custom node data with runtime type checking
    #     class Custom_Node_Data(Schema__MGraph__Node__Data):
    #         name: str
    #         value: int
    #         priority: float
    #
    #     # Type-safe node definition
    #     class Custom_Node(Schema__MGraph__Node):
    #         node_data: Custom_Node_Data
    #
    #     mgraph = MGraph()
    #     with mgraph.edit() as edit:
    #         # Create typed node
    #         node = edit.new_node(node_type=Custom_Node,
    #                             name="test",
    #                             value=42,
    #                             priority=1.5)
    #
    #         # Verify type safety
    #         assert node.node_data.name == "test"
    #         assert node.node_data.value == 42
    #         assert node.node_data.priority == 1.5
    #
    #         # Demonstrate type-safe processing
    #         result = node.node_data.priority * 2.0
    #         assert result == 3.0
    #
    # def test_index_system(self):
    #     """Test index system example from README"""
    #     # Custom node data with runtime type checking
    #     class Custom_Node_Data(Schema__MGraph__Node__Data):
    #         name: str
    #         value: int
    #         priority: float
    #
    #     # Type-safe node definition
    #     class Custom_Node(Schema__MGraph__Node):
    #         node_data: Custom_Node_Data
    #
    #     mgraph = MGraph()
    #     with mgraph.edit() as edit:
    #         # Create nodes
    #         node1 = edit.new_node(node_type=Custom_Node,
    #                              name="test",
    #                              value=42,
    #                              priority=1.5)
    #
    #         # Access index
    #         with edit.index() as index:
    #             # Get nodes by type
    #             nodes = index.get_nodes_by_type(Custom_Node)
    #             assert len(nodes) == 1
    #
    #             # Get by relationship
    #             nodes_by_type = index.get_nodes_by_type(Custom_Node)
    #             assert node1.node_id in nodes_by_type
    #
    # def test_export_and_visualization(self):
    #     """Test export and visualization example from README"""
    #     mgraph = MGraph()
    #     with mgraph.edit() as edit:
    #         # Create sample graph
    #         node1 = edit.new_node()
    #         node2 = edit.new_node()
    #         edge = edit.new_edge(from_node_id=node1.node_id,
    #                             to_node_id=node2.node_id)
    #
    #     # Test various export formats
    #     with mgraph.export() as export:
    #         # DOT format
    #         dot = export.to__dot()
    #         assert 'digraph' in dot
    #
    #         # Mermaid format
    #         mermaid = export.to__mermaid()
    #         assert 'graph TD' in mermaid
    #
    #         # GraphML format
    #         graphml = export.to__graphml()
    #         assert 'graphml' in graphml
    #
    #         # RDF/Turtle format
    #         turtle = export.to__turtle()
    #         assert '@prefix' in turtle
    #
    #     # Test visualization
    #     import os
    #     output_file = 'test_graph.png'
    #     with mgraph.screenshot() as screenshot:
    #         screenshot.save_to(output_file)
    #         assert os.path.exists(output_file)
    #         if os.path.exists(output_file):
    #             os.remove(output_file)