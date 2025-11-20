from typing                                                         import Optional, List
from mgraph_db.mgraph.MGraph                                        import MGraph
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph                   import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data           import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Types                 import Schema__MGraph__Types
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.utils.Misc                                         import random_int

class MGraph__Random_Graph(Type_Safe):
    graph        : MGraph                       = None
    graph__graph : Domain__MGraph__Graph        = None
    graph__model : Model__MGraph__Graph         = None
    graph__schema: Schema__MGraph__Graph        = None
    graph__data  : Schema__MGraph__Graph__Data  = None


    def setup(self) -> 'MGraph__Random_Graph':                                                                                            # Initialize all the graph components in the correct order
        self.graph__data   = Schema__MGraph__Graph__Data()
        self.graph__schema = Schema__MGraph__Graph (schema_types  = Schema__MGraph__Types(),
                                                    graph_type    = Schema__MGraph__Graph,
                                                    graph_data    = self.graph__data)
        self.graph__model = Model__MGraph__Graph   ( data          = self.graph__schema              )
        self.graph__graph = Domain__MGraph__Graph  ( model         = self.graph__model               )
        self.graph        = MGraph                 ( graph         = self.graph__graph               )
        return self

    def create_nodes(self, num_nodes: int) -> List[Obj_Id]:                                                        # Create specified number of nodes and return their IDs
        if num_nodes < 0:
            raise ValueError("Number of nodes cannot be negative")

        node_ids = []
        for _ in range(num_nodes):
            node = self.graph.edit().new_node()
            node_ids.append(node.node_id)
        return node_ids

    def create_random_edges(self, node_ids: List[Obj_Id], num_edges: int) -> None:                                 # Create random edges between existing nodes
        if not node_ids:
            raise ValueError("No nodes available to create edges")
        if num_edges < 0:
            raise ValueError("Number of edges cannot be negative")

        num_nodes = len(node_ids)
        for _ in range(num_edges):
            from_idx = random_int(max=num_nodes) - 1
            to_idx   = random_int(max=num_nodes) - 1

            self.graph.edit().new_edge(from_node_id = node_ids[from_idx],
                                       to_node_id   = node_ids[to_idx  ])

    def create_random_graph(self, num_nodes: int = 10, num_edges: Optional[int] = None) -> MGraph:                             # Create a new graph with random nodes and edges
        self.setup()
        if num_edges is None:
            num_edges = num_nodes * 2  # Default to twice as many edges as nodes

        node_ids = self.create_nodes(num_nodes)
        self.create_random_edges(node_ids, num_edges)

        return self.graph

def create_random_mgraph(num_nodes=2, num_edges=2) -> MGraph:                                        # Create an empty graph with no nodes or edges
    return MGraph__Random_Graph().setup().create_random_graph(num_nodes=num_nodes, num_edges=num_edges)

def create_empty_mgraph() -> MGraph:                                        # Create an empty graph with no nodes or edges
    return MGraph__Random_Graph().setup().graph