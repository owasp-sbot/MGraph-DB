from mgraph_db.mgraph.index.MGraph__Index__Edges                            import MGraph__Index__Edges
from mgraph_db.mgraph.index.MGraph__Index__Labels                           import MGraph__Index__Labels
from mgraph_db.mgraph.index.MGraph__Index__Paths                            import MGraph__Index__Paths
from mgraph_db.mgraph.index.MGraph__Index__Types                            import MGraph__Index__Types
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats            import Schema__MGraph__Index__Stats
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats            import Schema__MGraph__Index__Stats__Connections
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats            import Schema__MGraph__Index__Stats__Index_Data
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats            import Schema__MGraph__Index__Stats__Paths
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats            import Schema__MGraph__Index__Stats__Summary
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe


class MGraph__Index__Stats(Type_Safe):
    edges_index  : MGraph__Index__Edges  = None                                               # For edge counting
    labels_index : MGraph__Index__Labels = None                                               # For predicate counting
    paths_index  : MGraph__Index__Paths  = None                                               # For path counting
    types_index  : MGraph__Index__Types  = None                                               # For type counting

    # =========================================================================
    # Main Stats Method
    # =========================================================================

    def stats(self) -> Schema__MGraph__Index__Stats:
        return Schema__MGraph__Index__Stats(index_data = self.index_data_stats() ,
                                            summary    = self.summary_stats()    ,
                                            paths      = self.paths_stats()      )

    # =========================================================================
    # Component Stats Methods
    # =========================================================================

    def connections_stats(self) -> Schema__MGraph__Index__Stats__Connections:
        all_node_ids = (set(self.edges_index.data.nodes_to_incoming_edges.keys()) |
                        set(self.edges_index.data.nodes_to_outgoing_edges.keys()) )

        if not all_node_ids:
            return Schema__MGraph__Index__Stats__Connections()

        incoming_counts = [self.edges_index.count_node_incoming_edges(n) for n in all_node_ids]
        outgoing_counts = [self.edges_index.count_node_outgoing_edges(n) for n in all_node_ids]

        return Schema__MGraph__Index__Stats__Connections(
            total_nodes       = len(all_node_ids)                               ,
            avg_incoming_edges= round(sum(incoming_counts) / len(all_node_ids)) ,
            avg_outgoing_edges= round(sum(outgoing_counts) / len(all_node_ids)) ,
            max_incoming_edges= max(incoming_counts)                            ,
            max_outgoing_edges= max(outgoing_counts)                            )

    def summary_stats(self) -> Schema__MGraph__Index__Stats__Summary:
        return Schema__MGraph__Index__Stats__Summary(
            total_nodes       = sum(len(v) for v in self.types_index.data.nodes_by_type.values())    ,
            total_edges       = self.edges_index.edge_count()                                        ,
            total_predicates  = len(self.labels_index.data.edges_by_predicate)                       ,
            unique_node_paths = len(self.paths_index.data.nodes_by_path)                             ,
            unique_edge_paths = len(self.paths_index.data.edges_by_path)                             ,
            nodes_with_paths  = sum(len(v) for v in self.paths_index.data.nodes_by_path.values())    ,
            edges_with_paths  = sum(len(v) for v in self.paths_index.data.edges_by_path.values())    )

    def paths_stats(self) -> Schema__MGraph__Index__Stats__Paths:
        return Schema__MGraph__Index__Stats__Paths(
            node_paths = {str(k): len(v) for k, v in self.paths_index.data.nodes_by_path.items()}    ,
            edge_paths = {str(k): len(v) for k, v in self.paths_index.data.edges_by_path.items()}    )

    def index_data_stats(self) -> Schema__MGraph__Index__Stats__Index_Data:
        return Schema__MGraph__Index__Stats__Index_Data(
            edge_to_nodes         = self.edges_index.edge_count()                                           ,
            edges_by_type         = {k: len(v) for k, v in self.types_index.data.edges_by_type.items()}     ,
            edges_by_path         = {str(k): len(v) for k, v in self.paths_index.data.edges_by_path.items()},
            nodes_by_type         = {k: len(v) for k, v in self.types_index.data.nodes_by_type.items()}     ,
            nodes_by_path         = {str(k): len(v) for k, v in self.paths_index.data.nodes_by_path.items()},
            node_edge_connections = self.connections_stats()                                                )