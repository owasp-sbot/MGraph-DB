from typing                                                                 import Type, Set, Any, Dict, Optional
from mgraph_db.mgraph.index.MGraph__Index__Edges                            import MGraph__Index__Edges
from mgraph_db.mgraph.index.MGraph__Index__Labels                           import MGraph__Index__Labels
from mgraph_db.mgraph.index.MGraph__Index__Paths                            import MGraph__Index__Paths
from mgraph_db.mgraph.index.MGraph__Index__Types                            import MGraph__Index__Types
from mgraph_db.mgraph.index.MGraph__Index__Values                           import MGraph__Index__Values
from mgraph_db.mgraph.actions.MGraph__Type__Resolver                        import MGraph__Type__Resolver
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value                   import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                         import Edge_Path
from mgraph_db.mgraph.schemas.identifiers.Node_Path                         import Node_Path
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats            import Schema__MGraph__Index__Stats
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats            import Schema__MGraph__Index__Stats__Connections
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats            import Schema__MGraph__Index__Stats__Index_Data
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats            import Schema__MGraph__Index__Stats__Paths
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats            import Schema__MGraph__Index__Stats__Summary
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id           import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id           import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id           import Safe_Id
from osbot_utils.utils.Dev                                                  import pprint
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                          import Domain__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                          import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                          import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data             import Schema__MGraph__Index__Data
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.utils.Json                                                 import json_file_create, json_load_file


class MGraph__Index(Type_Safe):
    index_data   : Schema__MGraph__Index__Data                                              # Shared index data
    edges_index  : MGraph__Index__Edges                                                     # Edge-node structural indexing
    labels_index : MGraph__Index__Labels                                                    # Label indexing
    paths_index  : MGraph__Index__Paths                                                     # Path indexing
    types_index  : MGraph__Index__Types                                                     # Type indexing
    values_index : MGraph__Index__Values                                                    # Value node indexing
    resolver     : MGraph__Type__Resolver                                                   # Type resolution

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sync_index_data()

    def _sync_index_data(self) -> None:                                                     # Sync index_data reference to all sub-indexes
        self.edges_index.index_data  = self.index_data
        self.labels_index.index_data = self.index_data
        self.paths_index.index_data  = self.index_data
        self.types_index.index_data  = self.index_data

    # =========================================================================
    # Node Operations
    # =========================================================================

    def add_node(self, node: Schema__MGraph__Node) -> None:
        node_id        = node.node_id
        node_type      = self.resolver.node_type(node.node_type)
        node_type_name = node_type.__name__

        self.edges_index.init_node_edge_sets(node_id)
        self.types_index.index_node_type(node_id, node_type_name)
        self.paths_index.index_node_path(node)

        if node.node_type and issubclass(node.node_type, Schema__MGraph__Node__Value):
            self.values_index.add_value_node(node)

    def remove_node(self, node: Schema__MGraph__Node) -> None:
        node_id = node.node_id

        outgoing_edges, incoming_edges = self.edges_index.remove_node_edge_sets(node_id)

        for edge_id in outgoing_edges | incoming_edges:
            self.remove_edge_by_id(edge_id)

        node_type      = self.resolver.node_type(node.node_type)
        node_type_name = node_type.__name__

        self.types_index.remove_node_type(node_id, node_type_name)
        self.paths_index.remove_node_path(node)

        if node.node_type and issubclass(node.node_type, Schema__MGraph__Node__Value):
            self.values_index.remove_value_node(node)

    # =========================================================================
    # Edge Operations
    # =========================================================================

    def add_edge(self, edge: Schema__MGraph__Edge) -> None:
        edge_id        = edge.edge_id
        from_node_id   = edge.from_node_id
        to_node_id     = edge.to_node_id
        edge_type      = self.resolver.edge_type(edge.edge_type)
        edge_type_name = edge_type.__name__

        self.edges_index.index_edge(edge_id, from_node_id, to_node_id)
        self.labels_index.add_edge_label(edge)
        self.types_index.index_edge_type(edge_id, from_node_id, to_node_id, edge_type_name)
        self.paths_index.index_edge_path(edge)

    def remove_edge(self, edge: Schema__MGraph__Edge) -> 'MGraph__Index':
        self.remove_edge_by_id(edge.edge_id)
        return self

    def remove_edge_by_id(self, edge_id: Edge_Id) -> 'MGraph__Index':
        edge_type_name = self.index_data.edges_types.pop(edge_id, None)

        edge_nodes = self.edges_index.remove_edge(edge_id)
        if edge_nodes:
            from_node_id, to_node_id = edge_nodes
            self.types_index.remove_edge_type_by_node(edge_id, from_node_id, to_node_id, edge_type_name)

        self.types_index.remove_edge_type(edge_id, edge_type_name)
        self.paths_index.remove_edge_path_by_id(edge_id)
        self.labels_index.remove_edge_label_by_id(edge_id)
        return self

    # =========================================================================
    # Index Management
    # =========================================================================

    def load_index_from_graph(self, graph: Domain__MGraph__Graph) -> None:
        for node_id, node in graph.model.data.nodes.items():
            self.add_node(node)
        for edge_id, edge in graph.model.data.edges.items():
            self.add_edge(edge)

    def save_to_file(self, target_file: str) -> None:
        index_data = self.index_data.json()
        return json_file_create(index_data, target_file)

    # =========================================================================
    # Stats - Type_Safe Schema Based
    # =========================================================================

    def stats(self) -> Schema__MGraph__Index__Stats:
        return Schema__MGraph__Index__Stats(index_data = self._stats_index_data() ,
                                            summary    = self._stats_summary()    ,
                                            paths      = self._stats_paths()      )

    def _stats_connections(self) -> Schema__MGraph__Index__Stats__Connections:
        all_node_ids = (set(self.index_data.nodes_to_incoming_edges.keys()) |
                        set(self.index_data.nodes_to_outgoing_edges.keys()) )

        if not all_node_ids:
            return Schema__MGraph__Index__Stats__Connections()

        incoming_counts = [self.edges_index.count_node_incoming_edges(n) for n in all_node_ids]
        outgoing_counts = [self.edges_index.count_node_outgoing_edges(n) for n in all_node_ids]

        return Schema__MGraph__Index__Stats__Connections(
            total_nodes       = len(all_node_ids)                                       ,
            avg_incoming_edges= round(sum(incoming_counts) / len(all_node_ids))         ,
            avg_outgoing_edges= round(sum(outgoing_counts) / len(all_node_ids))         ,
            max_incoming_edges= max(incoming_counts)                                    ,
            max_outgoing_edges= max(outgoing_counts)                                    )

    def _stats_summary(self) -> Schema__MGraph__Index__Stats__Summary:
        return Schema__MGraph__Index__Stats__Summary(
            total_nodes       = sum(len(v) for v in self.index_data.nodes_by_type.values())   ,
            total_edges       = self.edges_index.edge_count()                                 ,
            total_predicates  = len(self.index_data.edges_by_predicate)                       ,
            unique_node_paths = len(self.index_data.nodes_by_path)                            ,
            unique_edge_paths = len(self.index_data.edges_by_path)                            ,
            nodes_with_paths  = sum(len(v) for v in self.index_data.nodes_by_path.values())   ,
            edges_with_paths  = sum(len(v) for v in self.index_data.edges_by_path.values())   )

    def _stats_paths(self) -> Schema__MGraph__Index__Stats__Paths:
        return Schema__MGraph__Index__Stats__Paths(
            node_paths = {str(k): len(v) for k, v in self.index_data.nodes_by_path.items()}   ,
            edge_paths = {str(k): len(v) for k, v in self.index_data.edges_by_path.items()}   )

    def _stats_index_data(self) -> Schema__MGraph__Index__Stats__Index_Data:
        return Schema__MGraph__Index__Stats__Index_Data(
            edge_to_nodes         = self.edges_index.edge_count()                                        ,
            edges_by_type         = {k: len(v) for k, v in self.index_data.edges_by_type.items()}        ,
            edges_by_path         = {str(k): len(v) for k, v in self.index_data.edges_by_path.items()}   ,
            nodes_by_type         = {k: len(v) for k, v in self.index_data.nodes_by_type.items()}        ,
            nodes_by_path         = {str(k): len(v) for k, v in self.index_data.nodes_by_path.items()}   ,
            node_edge_connections = self._stats_connections()                                            )

    def print__index_data(self):
        index_data = self.index_data.json()
        pprint(index_data)
        return index_data

    def print__stats(self):
        stats = self.stats()
        stats.print()
        return stats

    # =========================================================================
    # Query Methods - Values
    # =========================================================================

    def get_nodes_connected_to_value(self, value    : Any                                    ,
                                           edge_type: Type[Schema__MGraph__Edge       ] = None,
                                           node_type: Type[Schema__MGraph__Node__Value] = None
                                      ) -> Set[Node_Id]:
        value_type = type(value)
        if node_type is None:
            node_type = Schema__MGraph__Node__Value
        node_id = self.values_index.get_node_id_by_value(value_type=value_type, value=value, node_type=node_type)
        if not node_id:
            return set()

        incoming_edges = self.edges_index.get_node_id_incoming_edges(node_id)

        if edge_type:
            edge_type_name = edge_type.__name__
            incoming_edges = {e for e in incoming_edges if self.types_index.get_edge_type(e) == edge_type_name}

        return {self.edges_index.get_edge_from_node(e) for e in incoming_edges if self.edges_index.get_edge_from_node(e)}

    def get_node_connected_to_node__outgoing(self, node_id: Node_Id, edge_type: str) -> Optional[Node_Id]:
        connected_edges = self.types_index.get_node_outgoing_edges_by_type(node_id, edge_type)
        if connected_edges:
            edge_id = next(iter(connected_edges))
            return self.edges_index.get_edge_to_node(edge_id)
        return None

    # =========================================================================
    # Query Methods - Predicate/Label Based
    # =========================================================================

    def get_node_outgoing_edges_by_predicate(self, node_id: Node_Id, predicate: Safe_Id) -> Set[Edge_Id]:
        return self.edges_index.get_node_id_outgoing_edges(node_id) & self.labels_index.get_edges_by_predicate(predicate)

    def get_node_incoming_edges_by_predicate(self, node_id: Node_Id, predicate: Safe_Id) -> Set[Edge_Id]:
        return self.edges_index.get_node_id_incoming_edges(node_id) & self.labels_index.get_edges_by_predicate(predicate)

    def get_nodes_by_predicate(self, from_node_id: Node_Id, predicate: Safe_Id) -> Set[Node_Id]:
        edge_ids = self.get_node_outgoing_edges_by_predicate(from_node_id, predicate)
        return {self.edges_index.get_edge_to_node(e) for e in edge_ids if self.edges_index.get_edge_to_node(e)}

    # =========================================================================
    # Delegation - Edges Index
    # =========================================================================

    def get_node_outgoing_edges   (self, node   : Schema__MGraph__Node) -> Set[Edge_Id]: return self.edges_index.get_node_outgoing_edges(node)
    def get_node_incoming_edges   (self, node   : Schema__MGraph__Node) -> Set[Edge_Id]: return self.edges_index.get_node_incoming_edges(node)
    def get_node_id_outgoing_edges(self, node_id: Node_Id             ) -> Set[Edge_Id]: return self.edges_index.get_node_id_outgoing_edges(node_id)
    def get_node_id_incoming_edges(self, node_id: Node_Id             ) -> Set[Edge_Id]: return self.edges_index.get_node_id_incoming_edges(node_id)
    def edges_ids__from__node_id  (self, node_id: Node_Id             ) -> list        : return self.edges_index.edges_ids__from__node_id(node_id)
    def edges_ids__to__node_id    (self, node_id: Node_Id             ) -> list        : return self.edges_index.edges_ids__to__node_id(node_id)
    def nodes_ids__from__node_id  (self, node_id: Node_Id             ) -> list        : return self.edges_index.nodes_ids__from__node_id(node_id)

    # =========================================================================
    # Delegation - Types Index
    # =========================================================================

    def get_nodes_by_type(self, node_type: Type[Schema__MGraph__Node]) -> Set[Node_Id]: return self.types_index.get_nodes_by_type(node_type)
    def get_edges_by_type(self, edge_type: Type[Schema__MGraph__Edge]) -> Set[Edge_Id]: return self.types_index.get_edges_by_type(edge_type)

    # =========================================================================
    # Delegation - Labels Index
    # =========================================================================

    def get_edge_predicate         (self, edge_id  : Edge_Id) -> Optional[Safe_Id]: return self.labels_index.get_edge_predicate(edge_id)
    def get_edges_by_predicate     (self, predicate: Safe_Id) -> Set[Edge_Id]     : return self.labels_index.get_edges_by_predicate(predicate)
    def get_edges_by_incoming_label(self, label    : Safe_Id) -> Set[Edge_Id]     : return self.labels_index.get_edges_by_incoming_label(label)
    def get_edges_by_outgoing_label(self, label    : Safe_Id) -> Set[Edge_Id]     : return self.labels_index.get_edges_by_outgoing_label(label)

    # =========================================================================
    # Delegation - Paths Index
    # =========================================================================

    def get_nodes_by_path  (self, node_path: Node_Path) -> Set[Node_Id]       : return self.paths_index.get_nodes_by_path(node_path)
    def get_edges_by_path  (self, edge_path: Edge_Path) -> Set[Edge_Id]       : return self.paths_index.get_edges_by_path(edge_path)
    def get_all_node_paths (self                      ) -> Set[Node_Path]     : return self.paths_index.get_all_node_paths()
    def get_all_edge_paths (self                      ) -> Set[Edge_Path]     : return self.paths_index.get_all_edge_paths()
    def get_node_path      (self, node_id  : Node_Id  ) -> Optional[Node_Path]: return self.paths_index.get_node_path(node_id)
    def get_edge_path      (self, edge_id  : Edge_Id  ) -> Optional[Edge_Path]: return self.paths_index.get_edge_path(edge_id)
    def count_nodes_by_path(self, node_path: Node_Path) -> int                : return self.paths_index.count_nodes_by_path(node_path)
    def count_edges_by_path(self, edge_path: Edge_Path) -> int                : return self.paths_index.count_edges_by_path(edge_path)
    def has_node_path      (self, node_path: Node_Path) -> bool               : return self.paths_index.has_node_path(node_path)
    def has_edge_path      (self, edge_path: Edge_Path) -> bool               : return self.paths_index.has_edge_path(edge_path)

    # =========================================================================
    # Delegation - Backward Compatibility Methods
    # =========================================================================

    def index_node_path        (self, node: Schema__MGraph__Node) -> None: self.paths_index.index_node_path(node)
    def index_edge_path        (self, edge: Schema__MGraph__Edge) -> None: self.paths_index.index_edge_path(edge)
    def add_edge_label         (self, edge: Schema__MGraph__Edge) -> None: self.labels_index.add_edge_label(edge)
    def remove_node_type       (self, node: Schema__MGraph__Node) -> None: self.types_index.remove_node_type(node.node_id, self.resolver.node_type(node.node_type).__name__)
    def remove_node_path       (self, node: Schema__MGraph__Node) -> None: self.paths_index.remove_node_path(node)
    def remove_edge_path       (self, edge: Schema__MGraph__Edge) -> None: self.paths_index.remove_edge_path(edge)
    def remove_edge_label      (self, edge: Schema__MGraph__Edge) -> None: self.labels_index.remove_edge_label(edge)
    def _remove_edge_path_by_id (self, edge_id: Edge_Id)          -> None: self.paths_index.remove_edge_path_by_id(edge_id)
    def _remove_edge_label_by_id(self, edge_id: Edge_Id)          -> None: self.labels_index.remove_edge_label_by_id(edge_id)

    # =========================================================================
    # Raw Data Accessors (for backward compatibility)
    # =========================================================================

    def edges_to_nodes                 (self) -> Dict: return self.edges_index.edges_to_nodes()
    def edges_by_type                  (self) -> Dict: return self.types_index.edges_by_type()
    def edges_by_path                  (self) -> Dict: return self.paths_index.edges_by_path()
    def nodes_by_type                  (self) -> Dict: return self.types_index.nodes_by_type()
    def nodes_by_path                  (self) -> Dict: return self.paths_index.nodes_by_path()
    def nodes_to_incoming_edges        (self) -> Dict: return self.edges_index.nodes_to_incoming_edges()
    def nodes_to_incoming_edges_by_type(self) -> Dict: return self.types_index.nodes_to_incoming_edges_by_type()
    def nodes_to_outgoing_edges        (self) -> Dict: return self.edges_index.nodes_to_outgoing_edges()
    def nodes_to_outgoing_edges_by_type(self) -> Dict: return self.types_index.nodes_to_outgoing_edges_by_type()
    def edges_predicates               (self) -> Dict: return self.labels_index.edges_predicates()
    def edges_by_predicate_all         (self) -> Dict: return self.labels_index.edges_by_predicate()
    def edges_by_incoming_label        (self) -> Dict: return self.labels_index.edges_by_incoming_label()
    def edges_by_outgoing_label        (self) -> Dict: return self.labels_index.edges_by_outgoing_label()

    # =========================================================================
    # Factory Methods
    # =========================================================================

    @classmethod
    def from_graph(cls, graph: Domain__MGraph__Graph) -> 'MGraph__Index':
        with cls() as _:
            _.load_index_from_graph(graph)
            return _

    @classmethod
    def from_file(cls, source_file: str) -> 'MGraph__Index':
        with cls() as _:
            index_data_json = json_load_file(source_file)
            index_data      = Schema__MGraph__Index__Data.from_json(index_data_json)
            _.index_data    = index_data
            _._sync_index_data()
            return _