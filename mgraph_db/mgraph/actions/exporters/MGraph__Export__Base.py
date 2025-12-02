from typing                                          import Dict, Any, List
from mgraph_db.mgraph.actions.MGraph__Type__Resolver import MGraph__Type__Resolver
from mgraph_db.mgraph.domain.Domain__MGraph__Graph   import Domain__MGraph__Graph
from osbot_utils.type_safe.Type_Safe                 import Type_Safe

class Model__MGraph__Export__Context__Counters(Type_Safe):
    node  : int
    edge  : int
    other : int

class Model__MGraph__Export__Context(Type_Safe):
    nodes   : dict                                                                          # Store processed nodes
    edges   : dict                                                                          # Store processed edges
    counters: Model__MGraph__Export__Context__Counters                                      # ID generation counters

class MGraph__Export__Base(Type_Safe):
    graph   : Domain__MGraph__Graph                                                         # The graph to visualize
    context : Model__MGraph__Export__Context
    resolver: MGraph__Type__Resolver                                                        # Auto-instantiated - provides type resolution

    def generate_id(self, prefix: str) -> str:                                              # Generate unique IDs for elements
        if prefix == 'node':
            counter = self.context.counters.node
            self.context.counters.node = counter + 1
        elif prefix == 'edge':
            counter = self.context.counters.edge
            self.context.counters.edge = counter + 1
        else:
            counter = self.context.counters.other
            self.context.counters.other = counter + 1
        return f"{prefix}_{counter}"

    def process_graph(self) -> Dict[str, Any]:                                              # Process the entire graph and return visualization data
        for node in self.graph.nodes():                                                     # Process all nodes first
            self.process_node(node)

        for edge in self.graph.edges():                                                     # Then process all edges
            self.process_edge(edge)

        return self.format_output()

    def process_node(self, node) -> None:                                                   # Process a single node
        node_id = str(node.node_id)
        self.context.nodes[node_id] = self.create_node_data(node)

    def process_edge(self, edge) -> None:                                                   # Process a single edge
        edge_id = str(edge.edge_id)
        self.context.edges[edge_id] = self.create_edge_data(edge)

    def create_node_data(self, node) -> Dict[str, Any]:                                     # Create the data structure for a node - override in subclasses
        node_type = self.resolver.node_type(node.node.data.node_type)                       # Resolve type using resolver
        return {
            'id'  : str(node.node_id),
            'type': node_type.__name__
        }

    def create_edge_data(self, edge) -> Dict[str, Any]:                                     # Create the data structure for an edge - override in subclasses
        edge_type = self.resolver.edge_type(edge.edge.data.edge_type)                       # Resolve type using resolver
        return { 'id'    : str(edge.edge_id       )        ,
                 'source': str(edge.from_node_id())        ,
                 'target': str(edge.to_node_id  ())        ,
                 'type' : edge_type.__name__}

    def format_output(self) -> Dict[str, Any]:                                              # Format the processed data for visualization - override in subclasses"""
        return { 'nodes': list(self.context.nodes.values()),
                 'edges': list(self.context.edges.values())}

    def to_dict(self) -> Dict[str, Any]:                                                    # Convert graph to visualization format
        return self.process_graph()