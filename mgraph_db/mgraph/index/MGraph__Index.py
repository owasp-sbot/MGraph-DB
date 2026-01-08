from typing                                                                 import Type, Set, Dict, Optional
from mgraph_db.mgraph.index.MGraph__Index__Edges                            import MGraph__Index__Edges
from mgraph_db.mgraph.index.MGraph__Index__Edit                             import MGraph__Index__Edit
from mgraph_db.mgraph.index.MGraph__Index__Labels                           import MGraph__Index__Labels
from mgraph_db.mgraph.index.MGraph__Index__Paths                            import MGraph__Index__Paths
from mgraph_db.mgraph.index.MGraph__Index__Query                            import MGraph__Index__Query
from mgraph_db.mgraph.index.MGraph__Index__Stats                            import MGraph__Index__Stats
from mgraph_db.mgraph.index.MGraph__Index__Types                            import MGraph__Index__Types
from mgraph_db.mgraph.index.MGraph__Index__Values                           import MGraph__Index__Values
from mgraph_db.mgraph.actions.MGraph__Type__Resolver                        import MGraph__Type__Resolver
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                         import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                         import Edge_Path
from mgraph_db.mgraph.schemas.identifiers.Node_Path                         import Node_Path
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Config           import Schema__MGraph__Index__Config
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data             import Schema__MGraph__Index__Data
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats            import Schema__MGraph__Index__Stats
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id           import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id           import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id           import Safe_Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe              import type_safe
from osbot_utils.utils.Dev                                                  import pprint
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                          import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                          import Schema__MGraph__Edge
from osbot_utils.utils.Json                                                 import json_file_create, json_load_file


class MGraph__Index(Type_Safe):
    index_data   : Schema__MGraph__Index__Data                                                   # Composite index data (contains sub-schemas)
    index_config : Schema__MGraph__Index__Config    = None
    edges_index  : MGraph__Index__Edges                                                     # Edge-node structural indexing
    labels_index : MGraph__Index__Labels                                                    # Label indexing
    paths_index  : MGraph__Index__Paths                                                     # Path indexing
    types_index  : MGraph__Index__Types                                                     # Type indexing
    values_index : MGraph__Index__Values                                                    # Value node indexing

    # multiple dependencies injection
    edit_index   : MGraph__Index__Edit                   #                                  # Add/remove operations
    query_index  : MGraph__Index__Query                  #                                  # Complex cross-index queries
    stats_index  : MGraph__Index__Stats                  #                                  # Statistics calculation
    resolver     : MGraph__Type__Resolver                #                                  # Type resolution

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sync_index_data()

    def _sync_index_data(self) -> None:
        # Wire up each sub-index with its dedicated schema from index_data
        self.edges_index.data  = self.index_data.edges
        self.labels_index.data = self.index_data.labels
        self.paths_index.data  = self.index_data.paths
        self.types_index.data  = self.index_data.types


        # Wire up stats_index dependencies (uses sub-indexes directly)
        self.stats_index.edges_index  = self.edges_index
        self.stats_index.labels_index = self.labels_index
        self.stats_index.paths_index  = self.paths_index
        self.stats_index.types_index  = self.types_index

        # Wire up query_index dependencies
        self.query_index.edges_index  = self.edges_index
        self.query_index.labels_index = self.labels_index
        self.query_index.types_index  = self.types_index
        self.query_index.values_index = self.values_index

        # Wire up edit_index dependencies
        self.edit_index.edges_index  = self.edges_index
        self.edit_index.labels_index = self.labels_index
        self.edit_index.paths_index  = self.paths_index
        self.edit_index.types_index  = self.types_index
        self.edit_index.values_index = self.values_index
        self.edit_index.resolver     = self.resolver

    # =========================================================================
    # Node/Edge Operations (delegated to edit_index)
    # =========================================================================

    def add_node        (self, node: Schema__MGraph__Node   ) -> None            : self.edit_index.add_node(node)
    def remove_node     (self, node: Schema__MGraph__Node   ) -> None            : self.edit_index.remove_node(node)
    def add_edge        (self, edge: Schema__MGraph__Edge   ) -> None            : self.edit_index.add_edge(edge)
    def remove_edge     (self, edge: Schema__MGraph__Edge   ) -> 'MGraph__Index' : self.edit_index.remove_edge(edge); return self
    def remove_edge_by_id(self, edge_id: Edge_Id            ) -> 'MGraph__Index' : self.edit_index.remove_edge_by_id(edge_id); return self


    # =========================================================================
    # Stats (delegated to stats_index)
    # =========================================================================

    def stats(self) -> Schema__MGraph__Index__Stats:
        return self.stats_index.stats()

    def print__index_data(self):
        pprint(self.index_data.json())
        return self.index_data.json()

    def print__stats(self):
        stats = self.stats()
        stats.print()
        return stats

    # =========================================================================
    # Query Methods (delegated to query_index)
    # =========================================================================

    def get_nodes_connected_to_value        (self, value, edge_type=None, node_type=None) -> Set[Node_Id]      : return self.query_index.get_nodes_connected_to_value(value, edge_type, node_type)
    def get_node_connected_to_node__outgoing(self, node_id: Node_Id, edge_type: str     ) -> Optional[Node_Id] : return self.query_index.get_node_connected_to_node__outgoing(node_id, edge_type)
    def get_node_outgoing_edges_by_predicate(self, node_id: Node_Id, predicate: Safe_Id ) -> Set[Edge_Id]      : return self.query_index.get_node_outgoing_edges_by_predicate(node_id, predicate)
    def get_node_incoming_edges_by_predicate(self, node_id: Node_Id, predicate: Safe_Id ) -> Set[Edge_Id]      : return self.query_index.get_node_incoming_edges_by_predicate(node_id, predicate)
    def get_nodes_by_predicate              (self, from_node_id: Node_Id, predicate: Safe_Id) -> Set[Node_Id]  : return self.query_index.get_nodes_by_predicate(from_node_id, predicate)

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

    def index_node_path         (self, node: Schema__MGraph__Node) -> None: self.paths_index.index_node_path(node)
    def index_edge_path         (self, edge: Schema__MGraph__Edge) -> None: self.paths_index.index_edge_path(edge)
    def add_edge_label          (self, edge: Schema__MGraph__Edge) -> None: self.labels_index.add_edge_label(edge)
    def remove_node_type        (self, node: Schema__MGraph__Node) -> None: self.types_index.remove_node_type(node.node_id, self.resolver.node_type(node.node_type).__name__)
    def remove_node_path        (self, node: Schema__MGraph__Node) -> None: self.paths_index.remove_node_path(node)
    def remove_edge_path        (self, edge: Schema__MGraph__Edge) -> None: self.paths_index.remove_edge_path(edge)
    def remove_edge_label       (self, edge: Schema__MGraph__Edge) -> None: self.labels_index.remove_edge_label(edge)
    def _remove_edge_path_by_id (self, edge_id: Edge_Id)           -> None: self.paths_index.remove_edge_path_by_id(edge_id)
    def _remove_edge_label_by_id(self, edge_id: Edge_Id)           -> None: self.labels_index.remove_edge_label_by_id(edge_id)

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
    # Index Management
    # =========================================================================

    def load_index_from_graph(self, graph_data: Schema__MGraph__Graph) -> None:
        self.apply_config(graph_data)
        for node_id, node in graph_data.nodes.items():
            self.add_node(node)
        for edge_id, edge in graph_data.edges.items():
            self.add_edge(edge)

    def apply_config(self, graph_data: Schema__MGraph__Graph):
        if graph_data.index_config:
            with graph_data.index_config as _:
                self.index_config = _
                self.types_index.enabled  = _.types_enabled
                self.paths_index.enabled  = _.paths_enabled
                self.labels_index.enabled = _.labels_enabled
                self.values_index.enabled = _.values_enabled

    def save_to_file(self, target_file: str) -> None:
        return json_file_create(self.index_data.json(), target_file)

    @type_safe
    def reload(self, graph_data: Schema__MGraph__Graph) -> 'MGraph__Index':
        self.index_data = Schema__MGraph__Index__Data()                     # Fresh data
        self._sync_index_data()                                             # Re-wire sub-indexes
        self.load_index_from_graph(graph_data)                              # Rebuild
        return self

    # =========================================================================
    # Factory Methods
    # =========================================================================

    @classmethod
    def from_graph(cls, graph_data: Schema__MGraph__Graph) -> 'MGraph__Index':
        #with timestamp_block(name="from_graph.cls()"):
            with cls() as _:
                #with timestamp_block(name="from_graph.load()"):
                    _.load_index_from_graph(graph_data)
                    return _

    @classmethod
    def from_file(cls, source_file: str) -> 'MGraph__Index':
        with cls() as _:
            index_data_json = json_load_file(source_file)
            index_data      = Schema__MGraph__Index__Data.from_json(index_data_json)
            _.index_data    = index_data
            _._sync_index_data()
            return _