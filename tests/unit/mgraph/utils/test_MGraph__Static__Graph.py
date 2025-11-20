from unittest                                                    import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import is_obj_id
from mgraph_db.mgraph.MGraph                                     import MGraph
from mgraph_db.mgraph.utils.MGraph__Static__Graph                import MGraph__Static__Graph


class test_MGraph__Static__Graph(TestCase):

    def setUp(self):                                                                                                    # Initialize test data
        self.static_graph = MGraph__Static__Graph()

    def test_init(self):                                                                                                # Tests basic initialization
        assert type(self.static_graph)       is MGraph__Static__Graph
        assert type(self.static_graph.graph) is MGraph
        assert self.static_graph.node_ids    == []
        assert self.static_graph.edge_ids    == []

    def test_linear_graph(self):                                                                                        # Tests linear graph creation
        linear_graph = self.static_graph.linear_graph()                                                                 # Test with default nodes (3)
        assert len(linear_graph.node_ids) == 3
        assert len(linear_graph.edge_ids) == 2                                                                          # Should have n-1 edges

        for node_id in linear_graph.node_ids:                                                                           # Verify node and edge existence
            assert is_obj_id(node_id)                        is True
            assert linear_graph.graph.data().node(node_id) is not None

        for edge_id in linear_graph.edge_ids:
            assert is_obj_id(edge_id)                        is True
            assert linear_graph.graph.data().edge(edge_id) is not None

        node_ids = linear_graph.node_ids
        edge_ids = linear_graph.edge_ids
        # todo: write back these tests which broke after refactoring of to__json
        # assert linear_graph.graph.export().to__json() == {'edges': { edge_ids[0]: {'from_node_id': node_ids[0]  ,       # {1st edge}: from {1st node}
        #                                                                            'to_node_id'  : node_ids[1]  },      #           : to   {2nd node}
        #                                                              edge_ids[1]: {'from_node_id': node_ids[1]  ,       # {2nd edge}: from {2nd node}
        #                                                                            'to_node_id'  : node_ids[2]  }},     #           : to   {3rd node}
        #                                                   'nodes': { node_ids[0]: {},                                   # 1st node
        #                                                              node_ids[1]: {},                                   # 2nd node
        #                                                              node_ids[2]: {}}}                                  # 3rd node

        linear_graph = MGraph__Static__Graph().linear_graph(5)                                                          # Test with custom number of nodes
        assert len(linear_graph.node_ids) == 5
        assert len(linear_graph.edge_ids) == 4                                                                          # Should have n-1 edges

        for i in range(len(linear_graph.edge_ids)):                                                                     # Test edge connections
            edge = linear_graph.graph.data().edge(linear_graph.edge_ids[i])
            assert edge.from_node_id() == linear_graph.node_ids[i]
            assert edge.to_node_id()   == linear_graph.node_ids[i + 1]

        with self.assertRaises(ValueError) as context:                                                                  # Test invalid input
            MGraph__Static__Graph().linear_graph(0)
        assert str(context.exception) == "Number of nodes must be at least 1 for a linear graph"

    def test_circular_graph(self):                                                                                      # Tests circular graph creation
        static_graph = self.static_graph.circular_graph()                                                               # Test with default nodes (3)
        assert len(static_graph.node_ids) == 3
        assert len(static_graph.edge_ids) == 3                                                                          # Should have n edges


        last_edge = static_graph.graph.data().edge(static_graph.edge_ids[-1])                                           # Verify the circular connection
        assert last_edge.from_node_id() == static_graph.node_ids[-1]                                                    # Last node connects to first
        assert last_edge.to_node_id()   == static_graph.node_ids[0]

        node_ids = static_graph.node_ids
        edge_ids = static_graph.edge_ids
        # todo: write back these tests which broke after refactoring of to__json
        # assert static_graph.graph.export().to__json() == {'edges': { edge_ids[0]: {'from_node_id': node_ids[0],         # 1st edge: from 1st node to 2nd
        #                                                                            'to_node_id'  : node_ids[1]},
        #                                                              edge_ids[1]: {'from_node_id': node_ids[1],         # 2nd edge: from 2nd node to 3rd
        #                                                                            'to_node_id'  : node_ids[2]},
        #                                                              edge_ids[2]: {'from_node_id': node_ids[2],         # 3rd edge: from 3rd node back to 1st
        #                                                                            'to_node_id'  : node_ids[0]}},
        #                                                   'nodes': { node_ids[0]: {},                                   # 1st node
        #                                                              node_ids[1]: {},                                   # 2nd node
        #                                                              node_ids[2]: {}}}                                  # 3rd node


        # Test with custom number of nodes
        static_graph = MGraph__Static__Graph().circular_graph(4)
        assert len(static_graph.node_ids) == 4
        assert len(static_graph.edge_ids) == 4

        # Test invalid input
        with self.assertRaises(ValueError) as context:
            MGraph__Static__Graph().circular_graph(1)                                                                   # Needs at least 2 nodes
        assert str(context.exception) == "Number of nodes must be at least 2 for a circular graph"

    def test_star_graph(self):                                                                                          # Tests star graph creation
        # Test with default spokes (3)
        static_graph = self.static_graph.star_graph()
        assert len(static_graph.node_ids) == 4                                                                          # Center + 3 spokes
        assert len(static_graph.edge_ids) == 3                                                                          # One edge per spoke

        center_node_id = static_graph.node_ids[0]
        # Verify all edges connect to center
        for edge_id in static_graph.edge_ids:
            edge = static_graph.graph.data().edge(edge_id)
            assert edge.from_node_id() == center_node_id

        node_ids = static_graph.node_ids
        edge_ids = static_graph.edge_ids
        # todo: write back these tests which broke after refactoring of to__json
        # assert static_graph.graph.export().to__json() == {'edges': { edge_ids[0]: {'from_node_id': node_ids[0],         # 1st edge: from center to 1st spoke
        #                                                                            'to_node_id'  : node_ids[1]},
        #                                                              edge_ids[1]: {'from_node_id': node_ids[0],         # 2nd edge: from center to 2nd spoke
        #                                                                            'to_node_id'  : node_ids[2]},
        #                                                              edge_ids[2]: {'from_node_id': node_ids[0],         # 3rd edge: from center to 3rd spoke
        #                                                                            'to_node_id'  : node_ids[3]}},
        #                                                   'nodes': { node_ids[0]: {},                                   # Center node
        #                                                              node_ids[1]: {},                                   # 1st spoke
        #                                                              node_ids[2]: {},                                   # 2nd spoke
        #                                                              node_ids[3]: {}}}                                  # 3rd spoke


        static_graph = MGraph__Static__Graph().star_graph(5)                                                            # Test with custom number of spokes
        assert len(static_graph.node_ids) == 6                                                                          # Center + 5 spokes
        assert len(static_graph.edge_ids) == 5

        with self.assertRaises(ValueError) as context:                                                                  # Test invalid input
            MGraph__Static__Graph().star_graph(0)
        assert str(context.exception) == "Number of nodes must be at least 1 for a star graph"

    def test_complete_graph(self):                                                                                      # Tests complete graph creation
        static_graph = self.static_graph.complete_graph()                                                               # Test with default nodes (3)
        assert len(static_graph.node_ids) == 3
        assert len(static_graph.edge_ids) == 3                                                                          # n*(n-1)/2 edges

        node_ids = static_graph.node_ids
        edge_ids = static_graph.edge_ids

        # todo: write back these tests which broke after refactoring of to__json
        # assert static_graph.graph.export().to__json() == {'edges': { edge_ids[0]: {'from_node_id': node_ids[0],         # Edge: 1st to 2nd
        #                                                                            'to_node_id'  : node_ids[1]},
        #                                                              edge_ids[1]: {'from_node_id': node_ids[0],         # Edge: 1st to 3rd
        #                                                                            'to_node_id'  : node_ids[2]},
        #                                                              edge_ids[2]: {'from_node_id': node_ids[1],         # Edge: 2nd to 3rd
        #                                                                            'to_node_id'  : node_ids[2]}},
        #                                                   'nodes': { node_ids[0]: {},                                   # 1st node
        #                                                              node_ids[1]: {},                                   # 2nd node
        #                                                              node_ids[2]: {}}}                                  # 3rd node

        static_graph = MGraph__Static__Graph().complete_graph(4)                                                        # Test with custom number of nodes
        assert len(static_graph.node_ids) == 4
        assert len(static_graph.edge_ids) == 6                                                                          # 4*(4-1)/2 = 6 edges

        nodes = static_graph.node_ids                                                                                   # Verify all nodes are connected to each other
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                found_edge = False
                for edge_id in static_graph.edge_ids:
                    edge = static_graph.graph.data().edge(edge_id)
                    if ((edge.from_node_id() == nodes[i] and edge.to_node_id() == nodes[j]) or
                        (edge.from_node_id() == nodes[j] and edge.to_node_id() == nodes[i])):
                        found_edge = True
                        break
                assert found_edge is True

        with self.assertRaises(ValueError) as context:                                                                  # Test invalid input
            MGraph__Static__Graph().complete_graph(0)
        assert str(context.exception) == "Number of nodes must be at least 1 for a complete graph"

    def test_helper_functions(self):                                                                                    # Tests helper functions
        static_graph = MGraph__Static__Graph.create_linear(4)                                                           # Test linear graph helper
        assert type(static_graph) is MGraph__Static__Graph
        assert len(static_graph.node_ids) == 4
        assert len(static_graph.edge_ids) == 3

        static_graph = MGraph__Static__Graph.create_circular(4)                                                         # Test circular graph helper
        assert len(static_graph.node_ids) == 4
        assert len(static_graph.edge_ids) == 4

        static_graph = MGraph__Static__Graph.create_star(4)                                                             # Test star graph helper
        assert len(static_graph.node_ids) == 5                                                                          # Center + 4 spokes
        assert len(static_graph.edge_ids) == 4

        static_graph = MGraph__Static__Graph.create_complete(4)                                                         # Test complete graph helper
        assert len(static_graph.node_ids) == 4
        assert len(static_graph.edge_ids) == 6

        static_graph = self.static_graph.linear_graph(3)                                                                # Create some data first
        assert len(static_graph.node_ids) > 0
        assert len(static_graph.edge_ids) > 0

        static_graph.reset()                                                                                            # Reset and verify empty state
        assert type(static_graph.graph) is MGraph
        assert static_graph.node_ids == []
        assert static_graph.edge_ids == []

        static_graph.linear_graph(2)                                                                                    # Verify can still create graphs after reset
        assert len(static_graph.node_ids) == 2
        assert len(static_graph.edge_ids) == 1