from typing                                                              import Dict, Any, List
from mgraph_db.providers.mermaid.MGraph__Mermaid                         import MGraph__Mermaid
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Graph           import Domain__Mermaid__Graph
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id        import Safe_Id
from mgraph_db.mgraph.utils.MGraph__Random_Graph                         import MGraph__Random_Graph
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node           import Schema__Mermaid__Node
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge           import Schema__Mermaid__Edge
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data     import Schema__Mermaid__Node__Data
from mgraph_db.providers.mermaid.models.Model__Mermaid__Graph            import Model__Mermaid__Graph
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph          import Schema__Mermaid__Graph
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Types          import Schema__Mermaid__Types

class Mermaid__Random_Graph(MGraph__Random_Graph):

    def setup(self) -> 'Mermaid__Random_Graph':                                                                             # Initialize with Mermaid-specific components
        self.graph_data   = Schema__Mermaid__Graph        (schema_types = Schema__Mermaid__Types(),
                                                           graph_type   = Schema__Mermaid__Graph            ,
                                                           mermaid_code = []                                )
        self.graph__model = Model__Mermaid__Graph         (data=self.graph_data)

        self.graph__graph = Domain__Mermaid__Graph               (model         = self.graph__model)
        self.graph        = MGraph__Mermaid                      (graph         = self.graph__graph)
        return self

    def create_mermaid_node(self, key: str, label: str = None, value: Any = None) -> Schema__Mermaid__Node:             # create a Mermaid-specific node with the given parameters."""
        safe_key = Safe_Id(key)
        node_data = Schema__Mermaid__Node__Data ()
        return Schema__Mermaid__Node            ( node_data  = node_data                     ,
                                                  node_type  = Schema__Mermaid__Node       ,
                                                  key        = safe_key                    ,
                                                  label      = label or f"Label {safe_key}")

    def create_mermaid_edge(self, from_node: Schema__Mermaid__Node,                                                     # create a Mermaid-specific edge between nodes
                                  to_node  : Schema__Mermaid__Node,
                                  label    : str = None) -> Schema__Mermaid__Edge:

        return Schema__Mermaid__Edge               (edge_type      = Schema__Mermaid__Edge          ,
                                                    from_node_id   = from_node.node_id  ,
                                                    to_node_id     = to_node.node_id    ,
                                                    label          = label or f"Edge {from_node.key} to {to_node.key}")

    def create_nodes(self, num_nodes: int) -> List[Schema__Mermaid__Node]:                                             # Create specified number of Mermaid nodes
        if num_nodes < 0:
            raise ValueError("Number of nodes cannot be negative")

        nodes = []
        for i in range(num_nodes):
            node = self.create_mermaid_node(key=f'key_{i}')
            self.graph__model.add_node(node)
            nodes.append(node)
        return nodes

    def create_random_edges(self, nodes: List[Schema__Mermaid__Node], num_edges: int) -> None:                         # Create random edges between Mermaid nodes
        if not nodes:
            raise ValueError("No nodes available to create edges")
        if num_edges < 0:
            raise ValueError("Number of edges cannot be negative")

        from osbot_utils.utils.Misc import random_int
        num_nodes = len(nodes)

        for _ in range(num_edges):
            from_idx = random_int(max=num_nodes) - 1
            to_idx   = random_int(max=num_nodes) - 1

            edge = self.create_mermaid_edge(from_node = nodes[from_idx],
                                           to_node   = nodes[to_idx  ])
            self.graph__model.add_edge(edge)

    def create_test_graph(self, num_nodes: int = 3, num_edges: int = None) -> MGraph__Mermaid:                     # Create a test graph with nodes and edges
        if not self.graph__model:
            self.setup()

        nodes = self.create_nodes(num_nodes)

        if num_edges is None:
            num_edges = num_nodes * 2                                                                                    # Default to twice as many edges as nodes

        self.create_random_edges(nodes, num_edges)
        return self.graph

# Static helper functions
def create_test_mermaid_graph(num_nodes: int = 2, num_edges: int = 2) -> MGraph__Mermaid:                                    # Create a test Mermaid graph with the specified number of nodes and edges
    return Mermaid__Random_Graph().create_test_graph(num_nodes=num_nodes, num_edges=num_edges)

def create_empty_mermaid_graph() -> MGraph__Mermaid:                                                                            # Create an empty Mermaid graph
    return Mermaid__Random_Graph().setup().graph