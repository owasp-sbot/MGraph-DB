from typing                                                         import Type, Set, Any, Dict, Optional
from mgraph_db.mgraph.index.MGraph__Index__Paths                    import MGraph__Index__Paths
from mgraph_db.mgraph.index.MGraph__Index__Values                   import MGraph__Index__Values
from mgraph_db.mgraph.actions.MGraph__Type__Resolver                import MGraph__Type__Resolver
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value           import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                 import Edge_Path
from mgraph_db.mgraph.schemas.identifiers.Node_Path                 import Node_Path
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data import Schema__MGraph__Index__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id   import Safe_Id
from osbot_utils.utils.Dev                                          import pprint
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge

from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.utils.Json                                         import json_file_create, json_load_file


class MGraph__Index(Type_Safe):
    index_data  : Schema__MGraph__Index__Data                                               # Shared index data
    paths_index : MGraph__Index__Paths                                                      # Path indexing (extracted)
    values_index: MGraph__Index__Values                                                     # Value node indexing
    resolver    : MGraph__Type__Resolver                                                    # Auto-instantiated - provides type resolution

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paths_index.index_data = self.index_data                                       # Share index_data with paths_index

    # ---- Node operations ----

    def add_node(self, node: Schema__MGraph__Node) -> None:                                 # Add a node to the index
        node_id   = node.node_id
        node_type = self.resolver.node_type(node.node_type)                                 # Resolve type using resolver
        node_type_name = node_type.__name__

        self.index_data.nodes_types[node_id] = node_type_name

        if node_id not in self.index_data.nodes_to_outgoing_edges:                          # Initialize sets if needed
            self.index_data.nodes_to_outgoing_edges[node_id] = set()
        if node_id not in self.index_data.nodes_to_incoming_edges:
            self.index_data.nodes_to_incoming_edges[node_id] = set()

        if node_type_name not in self.index_data.nodes_by_type:                             # Add to type index
            self.index_data.nodes_by_type[node_type_name] = set()
        self.index_data.nodes_by_type[node_type_name].add(node_id)

        self.paths_index.index_node_path(node)                                              # Delegate to paths_index

        if node.node_type and issubclass(node.node_type, Schema__MGraph__Node__Value):      # if the data is a value
            self.values_index.add_value_node(node)                                          # add it to the index

    def index_node_path(self, node: Schema__MGraph__Node) -> None:                          # Delegate to paths_index
        self.paths_index.index_node_path(node)

    def remove_node(self, node: Schema__MGraph__Node) -> None:                              # Remove a node and all its references from the index
        node_id = node.node_id

        outgoing_edges = self.index_data.nodes_to_outgoing_edges.pop(node_id, set())        # Get associated edges before removing node references
        incoming_edges = self.index_data.nodes_to_incoming_edges.pop(node_id, set())

        for edge_id in outgoing_edges | incoming_edges:                                     # Clean up all connected edges
            self.remove_edge_by_id(edge_id)

        node_type = self.resolver.node_type(node.node_type)                                 # Resolve type using resolver
        node_type_name = node_type.__name__
        if node_type_name in self.index_data.nodes_by_type:
            self.index_data.nodes_by_type[node_type_name].discard(node_id)
            if not self.index_data.nodes_by_type[node_type_name]:
                del self.index_data.nodes_by_type[node_type_name]

        self.remove_node_type(node)
        self.paths_index.remove_node_path(node)                                             # Delegate to paths_index

        if node.node_type and issubclass(node.node_type, Schema__MGraph__Node__Value):
            self.values_index.remove_value_node(node)

    def remove_node_type(self, node: Schema__MGraph__Node) -> None:
        if node.node_id in self.index_data.nodes_types:
            del self.index_data.nodes_types[node.node_id]

    def remove_node_path(self, node: Schema__MGraph__Node) -> None:                         # Delegate to paths_index
        self.paths_index.remove_node_path(node)

    # ---- Edge operations ----

    def add_edge(self, edge: Schema__MGraph__Edge) -> None:                                 # Add an edge to the index
        edge_id      = edge.edge_id
        from_node_id = edge.from_node_id
        to_node_id   = edge.to_node_id
        edge_type    = self.resolver.edge_type(edge.edge_type)                              # Resolve type using resolver
        edge_type_name = edge_type.__name__

        self.add_edge_label(edge)

        self.index_data.edges_types   [edge_id] = edge_type_name
        self.index_data.edges_to_nodes[edge_id] = (from_node_id, to_node_id)


        if edge_type_name not in self.index_data.edges_by_type:                             # Add to type index
            self.index_data.edges_by_type[edge_type_name] = set()
        self.index_data.edges_by_type[edge_type_name].add(edge_id)

        if to_node_id not in self.index_data.nodes_to_incoming_edges_by_type:               # Update the new nodes_to_incoming_edges_by_type
            self.index_data.nodes_to_incoming_edges_by_type[to_node_id] = {}
        if edge_type_name not in self.index_data.nodes_to_incoming_edges_by_type[to_node_id]:
            self.index_data.nodes_to_incoming_edges_by_type[to_node_id][edge_type_name] = set()
        self.index_data.nodes_to_incoming_edges_by_type[to_node_id][edge_type_name].add(edge_id)


        if from_node_id not in self.index_data.nodes_to_outgoing_edges_by_type:             # Update the nodes_to_outgoing_edges_by_type index
            self.index_data.nodes_to_outgoing_edges_by_type[from_node_id] = {}
        if edge_type_name not in self.index_data.nodes_to_outgoing_edges_by_type[from_node_id]:
            self.index_data.nodes_to_outgoing_edges_by_type[from_node_id][edge_type_name] = set()
        self.index_data.nodes_to_outgoing_edges_by_type[from_node_id][edge_type_name].add(edge_id)

        if from_node_id not in self.index_data.nodes_to_outgoing_edges:                     # Add to node relationship indexes
            self.index_data.nodes_to_outgoing_edges[from_node_id] = set()
        self.index_data.nodes_to_outgoing_edges[from_node_id].add(edge_id)
        if to_node_id not in self.index_data.nodes_to_incoming_edges:
            self.index_data.nodes_to_incoming_edges[to_node_id] = set()
        self.index_data.nodes_to_incoming_edges[to_node_id].add(edge_id)

        self.paths_index.index_edge_path(edge)                                              # Delegate to paths_index

    def index_edge_path(self, edge: Schema__MGraph__Edge) -> None:                          # Delegate to paths_index
        self.paths_index.index_edge_path(edge)

    def add_edge_label(self, edge) -> None:
        if edge.edge_label:
            edge_id = edge.edge_id

            if edge.edge_label.predicate:                                                   # Index by predicate
                predicate = edge.edge_label.predicate
                self.index_data.edges_predicates[edge_id] = predicate                       # Store edge_id to predicate mapping

                if predicate not in self.index_data.edges_by_predicate:                     # Store predicate to edge_id mapping
                    self.index_data.edges_by_predicate[predicate] = set()
                self.index_data.edges_by_predicate[predicate].add(edge_id)

            if edge.edge_label.incoming:                                                    # Index by incoming label
                incoming = edge.edge_label.incoming
                self.index_data.edges_incoming_labels[edge_id] = incoming                   # store reverse mapping
                if incoming not in self.index_data.edges_by_incoming_label:
                    self.index_data.edges_by_incoming_label[incoming] = set()
                self.index_data.edges_by_incoming_label[incoming].add(edge_id)

            if edge.edge_label.outgoing:                                                    # Index by outgoing label
                outgoing = edge.edge_label.outgoing
                self.index_data.edges_outgoing_labels[edge_id] = outgoing                   # store reverse mapping
                if outgoing not in self.index_data.edges_by_outgoing_label:
                    self.index_data.edges_by_outgoing_label[outgoing] = set()
                self.index_data.edges_by_outgoing_label[outgoing].add(edge_id)

    def remove_edge(self, edge: Schema__MGraph__Edge) -> None:                              # Remove an edge and all its references from the index
        edge_id = edge.edge_id
        self.remove_edge_by_id(edge_id)
        return self

    def remove_edge_by_id(self, edge_id: Edge_Id) -> None:                                  # Remove edge using only its ID (data comes from index)
        edge_type_name = self.index_data.edges_types.pop(edge_id, None)

        if edge_id in self.index_data.edges_to_nodes:
            from_node_id, to_node_id = self.index_data.edges_to_nodes.pop(edge_id)
            self._remove_edge_node_references(edge_id, from_node_id, to_node_id, edge_type_name)

        self._remove_edge_type_reference(edge_id, edge_type_name)
        self.paths_index.remove_edge_path_by_id(edge_id)                                    # Delegate to paths_index
        self._remove_edge_label_by_id(edge_id)
        return self

    def _remove_edge_node_references(self, edge_id: Edge_Id, from_node_id: Node_Id,
                                           to_node_id: Node_Id, edge_type_name: str) -> None:
        # Basic mappings
        if from_node_id in self.index_data.nodes_to_outgoing_edges:
            self.index_data.nodes_to_outgoing_edges[from_node_id].discard(edge_id)
        if to_node_id in self.index_data.nodes_to_incoming_edges:
            self.index_data.nodes_to_incoming_edges[to_node_id].discard(edge_id)

        # Typed mappings - outgoing
        if edge_type_name and from_node_id in self.index_data.nodes_to_outgoing_edges_by_type:
            if edge_type_name in self.index_data.nodes_to_outgoing_edges_by_type[from_node_id]:
                self.index_data.nodes_to_outgoing_edges_by_type[from_node_id][edge_type_name].discard(edge_id)
                if not self.index_data.nodes_to_outgoing_edges_by_type[from_node_id][edge_type_name]:
                    del self.index_data.nodes_to_outgoing_edges_by_type[from_node_id][edge_type_name]
            if not self.index_data.nodes_to_outgoing_edges_by_type[from_node_id]:
                del self.index_data.nodes_to_outgoing_edges_by_type[from_node_id]

        # Typed mappings - incoming
        if edge_type_name and to_node_id in self.index_data.nodes_to_incoming_edges_by_type:
            if edge_type_name in self.index_data.nodes_to_incoming_edges_by_type[to_node_id]:
                self.index_data.nodes_to_incoming_edges_by_type[to_node_id][edge_type_name].discard(edge_id)
                if not self.index_data.nodes_to_incoming_edges_by_type[to_node_id][edge_type_name]:
                    del self.index_data.nodes_to_incoming_edges_by_type[to_node_id][edge_type_name]
            if not self.index_data.nodes_to_incoming_edges_by_type[to_node_id]:
                del self.index_data.nodes_to_incoming_edges_by_type[to_node_id]

    def _remove_edge_type_reference(self, edge_id: Edge_Id, edge_type_name: str) -> None:
        if edge_type_name and edge_type_name in self.index_data.edges_by_type:
            self.index_data.edges_by_type[edge_type_name].discard(edge_id)
            if not self.index_data.edges_by_type[edge_type_name]:
                del self.index_data.edges_by_type[edge_type_name]

    def _remove_edge_path_by_id(self, edge_id: Edge_Id) -> None:                            # Delegate to paths_index
        self.paths_index.remove_edge_path_by_id(edge_id)

    def _remove_edge_label_by_id(self, edge_id: Edge_Id) -> None:
        predicate = self.index_data.edges_predicates.pop(edge_id, None)                     # Remove from predicate indexes
        if predicate and predicate in self.index_data.edges_by_predicate:
            self.index_data.edges_by_predicate[predicate].discard(edge_id)
            if not self.index_data.edges_by_predicate[predicate]:
                del self.index_data.edges_by_predicate[predicate]

        incoming = self.index_data.edges_incoming_labels.pop(edge_id, None)                 # Remove from incoming label index
        if incoming and incoming in self.index_data.edges_by_incoming_label:
            self.index_data.edges_by_incoming_label[incoming].discard(edge_id)
            if not self.index_data.edges_by_incoming_label[incoming]:
                del self.index_data.edges_by_incoming_label[incoming]

        outgoing = self.index_data.edges_outgoing_labels.pop(edge_id, None)                 # Remove from outgoing label index
        if outgoing and outgoing in self.index_data.edges_by_outgoing_label:
            self.index_data.edges_by_outgoing_label[outgoing].discard(edge_id)
            if not self.index_data.edges_by_outgoing_label[outgoing]:
                del self.index_data.edges_by_outgoing_label[outgoing]

    def remove_edge_path(self, edge: Schema__MGraph__Edge) -> None:                         # Delegate to paths_index
        self.paths_index.remove_edge_path(edge)

    def remove_edge_label(self, edge) -> None:
        edge_id = edge.edge_id

        if edge.edge_label and edge.edge_label.predicate:                                   # Remove from predicate indexes
            predicate = edge.edge_label.predicate
            if predicate in self.index_data.edges_by_predicate:
                self.index_data.edges_by_predicate[predicate].discard(edge_id)
                if not self.index_data.edges_by_predicate[predicate]:
                    del self.index_data.edges_by_predicate[predicate]

            if edge_id in self.index_data.edges_predicates:
                del self.index_data.edges_predicates[edge_id]

        if edge.edge_label and edge.edge_label.incoming:                                    # Remove from incoming label index
            incoming = edge.edge_label.incoming
            if incoming in self.index_data.edges_by_incoming_label:
                self.index_data.edges_by_incoming_label[incoming].discard(edge_id)
                if not self.index_data.edges_by_incoming_label[incoming]:
                    del self.index_data.edges_by_incoming_label[incoming]

        if edge.edge_label and edge.edge_label.outgoing:                                    # Remove from outgoing label index
            outgoing = edge.edge_label.outgoing
            if outgoing in self.index_data.edges_by_outgoing_label:
                self.index_data.edges_by_outgoing_label[outgoing].discard(edge_id)
                if not self.index_data.edges_by_outgoing_label[outgoing]:
                    del self.index_data.edges_by_outgoing_label[outgoing]

    # ---- Path query methods (delegated to paths_index) ----

    def get_nodes_by_path(self, node_path: Node_Path) -> Set[Node_Id]:                      # Delegate to paths_index
        return self.paths_index.get_nodes_by_path(node_path)

    def get_edges_by_path(self, edge_path: Edge_Path) -> Set[Edge_Id]:                      # Delegate to paths_index
        return self.paths_index.get_edges_by_path(edge_path)

    # ---- Index management ----

    def load_index_from_graph(self, graph : Domain__MGraph__Graph) -> None:                 # Create index from existing graph
        for node_id, node in graph.model.data.nodes.items():                                # Add all nodes to index
            self.add_node(node)

        for edge_id, edge in graph.model.data.edges.items():                                # Add all edges to index
            self.add_edge(edge)

    def print__index_data(self):
        index_data = self.index_data.json()
        pprint(index_data)
        return index_data

    def print__stats(self):
        stats = self.stats()
        pprint(stats)
        return stats

    def save_to_file(self, target_file: str) -> None:                                       # Save index to file
        index_data = self.index_data.json()                                                 # get json (serialised) representation of the index object
        return json_file_create(index_data, target_file)                                    # save it to the target file

    # ---- Existing getters for data ----

    def get_edge_predicate(self, edge_id: Edge_Id):
        return self.index_data.edges_predicates.get(edge_id)

    def get_nodes_connected_to_value(self, value     : Any ,
                                           edge_type : Type[Schema__MGraph__Edge       ] = None ,
                                           node_type : Type[Schema__MGraph__Node__Value] = None
                                      ) -> Set[Node_Id]:                                    # Get nodes connected to a value node through optional edge type
        value_type = type(value)
        if node_type is None:
            node_type = Schema__MGraph__Node__Value
        node_id    = self.values_index.get_node_id_by_value(value_type=value_type, value=value, node_type=node_type)
        if not node_id:
            return set()

        connected_nodes = set()
        incoming_edges =  self.index_data.nodes_to_incoming_edges.get(node_id, set())

        if edge_type:
            edge_type_name = edge_type.__name__
            filtered_edges = set()
            for edge_id in incoming_edges:
                if self.index_data.edges_types[edge_id] == edge_type_name:
                    filtered_edges.add(edge_id)
            incoming_edges = filtered_edges

        for edge_id in incoming_edges:
            from_node_id, _ = self.edges_to_nodes()[edge_id]
            connected_nodes.add(from_node_id)

        return connected_nodes

    def get_node_connected_to_node__outgoing(self, node_id: Node_Id, edge_type: str) -> Optional[Node_Id]:
        connected_edges = self.index_data.nodes_to_outgoing_edges_by_type.get(node_id, {}).get(edge_type, set())

        if connected_edges:
            edge_id = next(iter(connected_edges))
            from_node_id, to_node_id = self.index_data.edges_to_nodes.get(edge_id, (None, None))
            return to_node_id

        return None

    def get_node_outgoing_edges(self, node: Schema__MGraph__Node) -> Set[Edge_Id]:
        return self.index_data.nodes_to_outgoing_edges.get(node.node_id, set())

    def get_node_id_outgoing_edges(self, node_id: Node_Id) -> Set[Edge_Id]:
        return self.index_data.nodes_to_outgoing_edges.get(node_id, set())

    def get_node_id_incoming_edges(self, node_id: Node_Id) -> Set[Edge_Id]:
        return self.index_data.nodes_to_incoming_edges.get(node_id, set())

    def get_node_incoming_edges(self, node: Schema__MGraph__Node) -> Set[Edge_Id]:
        return self.index_data.nodes_to_incoming_edges.get(node.node_id, set())

    def get_nodes_by_type(self, node_type: Type[Schema__MGraph__Node]) -> Set[Node_Id]:
        return self.index_data.nodes_by_type.get(node_type.__name__, set())

    def get_edges_by_type(self, edge_type: Type[Schema__MGraph__Edge]) -> Set[Edge_Id]:
        return self.index_data.edges_by_type.get(edge_type.__name__, set())


    # ============================================================================
    # Stats
    # ============================================================================

    def stats(self) -> Dict[str, Any]:                                              # Returns statistical summary of index data
        edge_counts = {                                                             # Calculate total edges per node
            node_id: {
                'incoming': len(self.index_data.nodes_to_incoming_edges.get(node_id, [])),
                'outgoing': len(self.index_data.nodes_to_outgoing_edges.get(node_id, []))
            }
            for node_id in set(self.index_data.nodes_to_incoming_edges.keys()) |
                           set(self.index_data.nodes_to_outgoing_edges.keys())
        }
        avg_incoming_edges = sum(n['incoming'] for n in edge_counts.values()) / len(edge_counts) if edge_counts else 0
        avg_outgoing_edges = sum(n['outgoing'] for n in edge_counts.values()) / len(edge_counts) if edge_counts else 0

        stats_data = {
            'index_data': {
                'edge_to_nodes'         : len(self.index_data.edges_to_nodes)                          ,
                'edges_by_type'         : {k: len(v) for k, v in
                                           self.index_data.edges_by_type.items()}                      ,
                'edges_by_path'         : {str(k): len(v) for k, v in
                                           self.index_data.edges_by_path.items()}                      ,
                'nodes_by_type'         : {k: len(v) for k, v in
                                           self.index_data.nodes_by_type.items()}                      ,
                'nodes_by_path'         : {str(k): len(v) for k, v in
                                           self.index_data.nodes_by_path.items()}                      ,
                'node_edge_connections' : {
                    'total_nodes'       : len(edge_counts)                                             ,
                    'avg_incoming_edges': round(avg_incoming_edges)                                    ,
                    'avg_outgoing_edges': round(avg_outgoing_edges)                                    ,
                    'max_incoming_edges': max((n['incoming'] for n in edge_counts.values()), default=0),
                    'max_outgoing_edges': max((n['outgoing'] for n in edge_counts.values()), default=0)
                }
            },
            'summary': {                                                                                # REST-friendly summary
                'total_nodes'      : sum(len(v) for v in self.index_data.nodes_by_type.values())       ,
                'total_edges'      : len(self.index_data.edges_to_nodes)                               ,
                'total_predicates' : len(self.index_data.edges_by_predicate)                           ,
                'unique_node_paths': len(self.index_data.nodes_by_path)                                ,
                'unique_edge_paths': len(self.index_data.edges_by_path)                                ,
                'nodes_with_paths' : sum(len(v) for v in self.index_data.nodes_by_path.values())       ,
                'edges_with_paths' : sum(len(v) for v in self.index_data.edges_by_path.values())       ,
            },
            'paths': {                                                                                  # Dedicated path section
                'node_paths': {str(k): len(v) for k, v in self.index_data.nodes_by_path.items()}       ,
                'edge_paths': {str(k): len(v) for k, v in self.index_data.edges_by_path.items()}       ,
            }
        }

        return stats_data


    # ============================================================================
    # Edge label helpers
    # ============================================================================

    def get_edges_by_predicate(self, predicate: Safe_Id) -> Set[Edge_Id]:        # Get edges by predicate
        return self.index_data.edges_by_predicate.get(predicate, set())

    def get_edges_by_incoming_label(self, label: Safe_Id) -> Set[Edge_Id]:       # Get edges by incoming label
        return self.index_data.edges_by_incoming_label.get(label, set())

    def get_edges_by_outgoing_label(self, label: Safe_Id) -> Set[Edge_Id]:       # Get edges by outgoing label
        return self.index_data.edges_by_outgoing_label.get(label, set())

    def get_node_outgoing_edges_by_predicate(self, node_id  : Node_Id ,
                                                   predicate: Safe_Id
                                              ) -> Set[Edge_Id]:                 # Get outgoing edges by predicate
        outgoing_edges  = self.get_node_id_outgoing_edges(node_id)
        predicate_edges = self.get_edges_by_predicate(predicate)
        return outgoing_edges & predicate_edges

    def get_node_incoming_edges_by_predicate(self, node_id  : Node_Id ,
                                                   predicate: Safe_Id
                                              ) -> Set[Edge_Id]:                 # Get incoming edges by predicate
        incoming_edges  = self.get_node_id_incoming_edges(node_id)
        predicate_edges = self.get_edges_by_predicate(predicate)
        return incoming_edges & predicate_edges

    def get_nodes_by_predicate(self, from_node_id: Node_Id ,
                                     predicate   : Safe_Id
                                ) -> Set[Node_Id]:                               # Get target nodes via predicate
        edge_ids = self.get_node_outgoing_edges_by_predicate(from_node_id, predicate)
        result   = set()
        for edge_id in edge_ids:
            _, to_node_id = self.index_data.edges_to_nodes.get(edge_id, (None, None))
            if to_node_id:
                result.add(to_node_id)
        return result

    # ============================================================================
    # Path Query Methods (delegated to paths_index)
    # ============================================================================

    def get_all_node_paths(self) -> Set[Node_Path]:                              # Delegate to paths_index
        return self.paths_index.get_all_node_paths()

    def get_all_edge_paths(self) -> Set[Edge_Path]:                              # Delegate to paths_index
        return self.paths_index.get_all_edge_paths()

    def get_node_path(self, node_id: Node_Id) -> Optional[Node_Path]:            # Delegate to paths_index
        return self.paths_index.get_node_path(node_id)

    def get_edge_path(self, edge_id: Edge_Id) -> Optional[Edge_Path]:            # Delegate to paths_index
        return self.paths_index.get_edge_path(edge_id)

    def count_nodes_by_path(self, node_path: Node_Path) -> int:                  # Delegate to paths_index
        return self.paths_index.count_nodes_by_path(node_path)

    def count_edges_by_path(self, edge_path: Edge_Path) -> int:                  # Delegate to paths_index
        return self.paths_index.count_edges_by_path(edge_path)

    def has_node_path(self, node_path: Node_Path) -> bool:                       # Delegate to paths_index
        return self.paths_index.has_node_path(node_path)

    def has_edge_path(self, edge_path: Edge_Path) -> bool:                       # Delegate to paths_index
        return self.paths_index.has_edge_path(edge_path)


    # ---- Raw data accessors ----

    def edges_to_nodes                 (self): return self.index_data.edges_to_nodes
    def edges_by_type                  (self): return self.index_data.edges_by_type
    def edges_by_path                  (self): return self.paths_index.edges_by_path()                   # Delegate to paths_index
    def nodes_by_type                  (self): return self.index_data.nodes_by_type
    def nodes_by_path                  (self): return self.paths_index.nodes_by_path()                   # Delegate to paths_index
    def nodes_to_incoming_edges        (self): return self.index_data.nodes_to_incoming_edges
    def nodes_to_incoming_edges_by_type(self): return self.index_data.nodes_to_incoming_edges_by_type
    def nodes_to_outgoing_edges        (self): return self.index_data.nodes_to_outgoing_edges
    def nodes_to_outgoing_edges_by_type(self): return  self.index_data.nodes_to_outgoing_edges_by_type

    def edges_predicates               (self) -> Dict[Edge_Id, Safe_Id]      : return self.index_data.edges_predicates
    def edges_by_predicate_all         (self) -> Dict[Safe_Id, Set[Edge_Id]] : return self.index_data.edges_by_predicate       # Raw accessor (avoid conflict with query method)
    def edges_by_incoming_label        (self) -> Dict[Safe_Id, Set[Edge_Id]] : return self.index_data.edges_by_incoming_label
    def edges_by_outgoing_label        (self) -> Dict[Safe_Id, Set[Edge_Id]] : return self.index_data.edges_by_outgoing_label


    def edges_ids__from__node_id(self, node_id) -> list:
        with self.index_data as _:
            return list(_.nodes_to_outgoing_edges.get(node_id, {}))

    def edges_ids__to__node_id(self, node_id) -> list:
        with self.index_data as _:
            return list(_.nodes_to_incoming_edges.get(node_id, {}))

    def nodes_ids__from__node_id(self, node_id) -> list:
        with self.index_data as _:
            nodes_ids = []
            for edge_id in self.edges_ids__from__node_id(node_id):
                (from_node_id, to_node_id) = _.edges_to_nodes[edge_id]
                nodes_ids.append(to_node_id)
            return nodes_ids



    # ---- Factory methods ----

    @classmethod
    def from_graph(cls, graph: Domain__MGraph__Graph) -> 'MGraph__Index':
        with cls() as _:
            _.load_index_from_graph(graph)
            return _

    @classmethod
    def from_file(cls, source_file: str) -> 'MGraph__Index':
        with cls() as _:
            index_data__json         = json_load_file(source_file)
            index_data               = Schema__MGraph__Index__Data.from_json(index_data__json)
            _.index_data             = index_data
            _.paths_index.index_data = index_data
            return _