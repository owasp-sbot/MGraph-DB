from typing                         import Dict
from osbot_utils.type_safe.Type_Safe import Type_Safe

# todo: refactor these into separate files (one file per schema)
class Schema__MGraph__Index__Stats__Connections(Type_Safe):                              # Node-edge connection statistics
    total_nodes      : int = 0
    avg_incoming_edges: int = 0
    avg_outgoing_edges: int = 0
    max_incoming_edges: int = 0
    max_outgoing_edges: int = 0


class Schema__MGraph__Index__Stats__Summary(Type_Safe):                                  # High-level summary stats (REST-friendly)
    total_nodes      : int = 0
    total_edges      : int = 0
    total_predicates : int = 0
    unique_node_paths: int = 0
    unique_edge_paths: int = 0
    nodes_with_paths : int = 0
    edges_with_paths : int = 0


class Schema__MGraph__Index__Stats__Paths(Type_Safe):                                    # Path statistics
    node_paths: Dict[str, int]                                                           # path -> count of nodes
    edge_paths: Dict[str, int]                                                           # path -> count of edges


class Schema__MGraph__Index__Stats__Index_Data(Type_Safe):                               # Detailed index data stats
    edge_to_nodes        : int = 0
    edges_by_type        : Dict[str, int]                                                # type -> count
    edges_by_path        : Dict[str, int]                                                # path -> count
    nodes_by_type        : Dict[str, int]                                                # type -> count
    nodes_by_path        : Dict[str, int]                                                # path -> count
    node_edge_connections: Schema__MGraph__Index__Stats__Connections


class Schema__MGraph__Index__Stats(Type_Safe):                                           # Main stats container
    index_data: Schema__MGraph__Index__Stats__Index_Data
    summary   : Schema__MGraph__Index__Stats__Summary
    paths     : Schema__MGraph__Index__Stats__Paths