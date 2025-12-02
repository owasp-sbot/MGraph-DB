from typing                                                         import List
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.MGraph                                        import MGraph
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe

class MGraph__Static__Graph(Type_Safe):
    graph   : MGraph
    node_ids: List[Obj_Id]
    edge_ids: List[Obj_Id]

    def create_nodes(self, count: int) -> List[Obj_Id]:                                                          # Creates specified number of nodes
        with self.graph.edit() as edit:
            return [edit.new_node(node_type=Schema__MGraph__Node).node_id for _ in range(count)]

    def validate_node_count(self, num_nodes: int, min_nodes: int, graph_type: str):                                   # Validates minimum number of nodes for graph type
        if num_nodes < min_nodes:
            raise ValueError(f"Number of nodes must be at least {min_nodes} for a {graph_type}")

    def create_edge(self, from_node: Obj_Id, to_node: Obj_Id) -> Obj_Id:                               # Creates an edge between two nodes
        with self.graph.edit() as edit:
            edge = edit.new_edge(from_node_id=from_node, to_node_id=to_node)
            self.edge_ids.append(edge.edge_id)
            return edge.edge_id

    def linear_graph(self, num_nodes: int = 3) -> 'MGraph__Static__Graph':                                           # Creates a linear graph where each node connects to the next node in sequence
        self.validate_node_count(num_nodes, 1, "linear graph")

        with self.graph.edit() as edit:
            self.node_ids = self.create_nodes(num_nodes)                                                              # Create nodes
            for i in range(num_nodes - 1):                                                                            # Create edges connecting nodes linearly
                self.create_edge(self.node_ids[i], self.node_ids[i + 1])
        return self

    def circular_graph(self, num_nodes: int = 3) -> 'MGraph__Static__Graph':                                         # Creates a circular graph where each node connects to the next node in sequence, and the last node connects back to the first
        self.validate_node_count(num_nodes, 2, "circular graph")

        with self.graph.edit() as edit:
            self.node_ids = self.create_nodes(num_nodes)                                                              # First create a linear graph
            for i in range(num_nodes - 1):
                self.create_edge(self.node_ids[i], self.node_ids[i + 1])
            self.create_edge(self.node_ids[-1], self.node_ids[0])                                                    # Add the final edge to complete the circle
        return self

    def star_graph(self, num_spokes: int = 3) -> 'MGraph__Static__Graph':                                           # Creates a star graph with a central node connected to multiple spoke nodes
        self.validate_node_count(num_spokes, 1, "star graph")

        with self.graph.edit() as edit:
            self.node_ids = self.create_nodes(num_spokes + 1)                                                        # Create central node and spokes
            center_node = self.node_ids[0]
            for i in range(1, num_spokes + 1):                                                                       # Create edges from center to each spoke
                self.create_edge(center_node, self.node_ids[i])
        return self

    def complete_graph(self, num_nodes: int = 3) -> 'MGraph__Static__Graph':                                        # Creates a complete graph where every node is connected to every other node
        self.validate_node_count(num_nodes, 1, "complete graph")

        with self.graph.edit() as edit:
            self.node_ids = self.create_nodes(num_nodes)                                                             # Create all nodes
            for i in range(num_nodes):                                                                               # Connect each node to every other node
                for j in range(i + 1, num_nodes):
                    self.create_edge(self.node_ids[i], self.node_ids[j])
        return self

    @classmethod
    def create_linear(cls, num_nodes: int = 3) -> 'MGraph__Static__Graph':                                          # Factory method for linear graph
        return cls().linear_graph(num_nodes)

    @classmethod
    def create_circular(cls, num_nodes: int = 3) -> 'MGraph__Static__Graph':                                        # Factory method for circular graph
        return cls().circular_graph(num_nodes)

    @classmethod
    def create_star(cls, num_spokes: int = 3) -> 'MGraph__Static__Graph':                                          # Factory method for star graph
        return cls().star_graph(num_spokes)

    @classmethod
    def create_complete(cls, num_nodes: int = 3) -> 'MGraph__Static__Graph':                                       # Factory method for complete graph
        return cls().complete_graph(num_nodes)

    def reset(self):                                                                                                # Resets the graph to initial state
        self.graph = MGraph()
        self.node_ids = []
        self.edge_ids = []
        return self