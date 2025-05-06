from typing                                          import Type, Optional, Set, List
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge   import Schema__MGraph__Edge
from mgraph_db.query.domain.Domain__MGraph__Query    import Domain__MGraph__Query
from osbot_utils.type_safe.Type_Safe                 import Type_Safe


class MGraph__Query__Navigate(Type_Safe):
    query: Domain__MGraph__Query                                                   # Reference to domain query

    def to_connected_nodes(self,edge_type: Optional[Type[Schema__MGraph__Edge]] = None,
                                direction: str = 'outgoing'
                          ) -> 'MGraph__Query__Navigate':                          # Navigate to connected nodes in specified direction, optionally filtered by edge type.
        current_nodes, _ = self.query.get_current_ids()
        connected_nodes = set()
        connected_edges = set()

        for node_id in current_nodes:
            node = self.query.mgraph_data.node(node_id)
            if node:
                if direction == 'outgoing':                                                         # Get edges based on direction
                    edges = self.query.mgraph_index.get_node_id_outgoing_edges(node_id)
                elif direction == 'incoming':
                    edges = self.query.mgraph_index.get_node_id_incoming_edges(node_id)
                else:
                    raise ValueError(f"Invalid direction: {direction}")

                # Filter by edge type if specified
                if edge_type:
                    edges = {edge_id for edge_id in edges
                            if edge_id and
                            self.query.mgraph_data.edge(edge_id) and
                            isinstance(self.query.mgraph_data.edge(edge_id).edge.data, edge_type)}

                # Get connected nodes
                for edge_id in edges:
                    edge = self.query.mgraph_data.edge(edge_id)
                    if edge:
                        connected_edges.add(edge_id)
                        if direction == 'outgoing':
                            connected_nodes.add(edge.to_node_id())
                        else:
                            connected_nodes.add(edge.from_node_id())

        self.query.create_view(nodes_ids = connected_nodes,
                              edges_ids = connected_edges,
                              operation = 'to_connected_nodes',
                              params    = {'edge_type': edge_type.__name__ if edge_type else None,
                                          'direction': direction})
        return self

    # def to_outgoing(self,
    #                  edge_type: Optional[Type[Schema__MGraph__Edge]] = None
    #                 ) -> 'MGraph__Query__Navigate':
    #     """Navigate to nodes connected by outgoing edges."""
    #     return self.to_connected_nodes(edge_type=edge_type, direction='outgoing')
    #
    # def to_incoming(self,
    #                  edge_type: Optional[Type[Schema__MGraph__Edge]] = None
    #                 ) -> 'MGraph__Query__Navigate':
    #     """Navigate to nodes connected by incoming edges."""
    #     return self.to_connected_nodes(edge_type=edge_type, direction='incoming')
    #
    # def follow_path(self, edge_types: List[Type[Schema__MGraph__Edge]]) -> 'MGraph__Query__Navigate':
    #     """Follow a path of edges defined by a sequence of edge types."""
    #     for edge_type in edge_types:
    #         self.to_outgoing(edge_type)
    #     return self
    #
    # def to_root(self) -> 'MGraph__Query__Navigate':
    #     """Navigate to root nodes (nodes without incoming edges)."""
    #     current_nodes, _ = self.query.get_current_ids()
    #     root_nodes = set()
    #     edges_to_roots = set()
    #
    #     for node_id in current_nodes:
    #         current_node_id = node_id
    #         path_to_root = []  # Track the path to root
    #
    #         while True:
    #             incoming_edges = self.query.mgraph_index.edges_ids__to__node_id(current_node_id)
    #             if not incoming_edges:  # Found a root node
    #                 root_nodes.add(current_node_id)
    #                 # Add all edges in the path to the root
    #                 edges_to_roots.update(path_to_root)
    #                 break
    #
    #             edge_id = incoming_edges[0]  # Take first incoming edge
    #             path_to_root.append(edge_id)
    #
    #             edge = self.query.mgraph_data.edge(edge_id)
    #             if not edge:  # Safety check
    #                 break
    #
    #             current_node_id = edge.from_node_id()
    #             if current_node_id in root_nodes or not current_node_id:  # Avoid cycles
    #                 edges_to_roots.update(path_to_root)
    #                 break
    #
    #     self.query.create_view(nodes_ids = root_nodes,
    #                           edges_ids = edges_to_roots,
    #                           operation = 'to_root',
    #                           params    = {})
    #     return self
    #
    # def to_children(self) -> 'MGraph__Query__Navigate':
    #     """Navigate to direct children of current nodes (for HTML document traversal)."""
    #     return self.to_outgoing()
    #
    # def to_parent(self) -> 'MGraph__Query__Navigate':
    #     """Navigate to the parent of current nodes (for HTML document traversal)."""
    #     return self.to_incoming()
    #
    # def to_siblings(self) -> 'MGraph__Query__Navigate':
    #     """Navigate to siblings (nodes with the same parent)."""
    #     current_nodes, _ = self.query.get_current_ids()
    #     sibling_nodes = set()
    #     connection_edges = set()
    #
    #     # First find parents
    #     for node_id in current_nodes:
    #         incoming_edges = self.query.mgraph_index.edges_ids__to__node_id(node_id)
    #         for edge_id in incoming_edges:
    #             edge = self.query.mgraph_data.edge(edge_id)
    #             if edge:
    #                 parent_id = edge.from_node_id()
    #                 # Then find all children of those parents
    #                 outgoing_edges = self.query.mgraph_index.edges_ids__from__node_id(parent_id)
    #                 for child_edge_id in outgoing_edges:
    #                     child_edge = self.query.mgraph_data.edge(child_edge_id)
    #                     if child_edge:
    #                         child_node_id = child_edge.to_node_id()
    #                         if child_node_id != node_id:  # Exclude self
    #                             sibling_nodes.add(child_node_id)
    #                             connection_edges.add(child_edge_id)
    #
    #     self.query.create_view(nodes_ids = sibling_nodes,
    #                           edges_ids = connection_edges,
    #                           operation = 'to_siblings',
    #                           params    = {})
    #     return self
    #
    # def to_descendants(self, max_depth: Optional[int] = None) -> 'MGraph__Query__Navigate':
    #     """Navigate to all descendants (children, grandchildren, etc.) up to max_depth."""
    #     current_nodes, _ = self.query.get_current_ids()
    #     all_descendants = set()
    #     all_edges = set()
    #
    #     def collect_descendants(node_id: Obj_Id, current_depth: int):
    #         if max_depth is not None and current_depth > max_depth:
    #             return
    #
    #         outgoing_edges = self.query.mgraph_index.edges_ids__from__node_id(node_id)
    #         for edge_id in outgoing_edges:
    #             edge = self.query.mgraph_data.edge(edge_id)
    #             if edge:
    #                 child_id = edge.to_node_id()
    #                 if child_id not in all_descendants:
    #                     all_descendants.add(child_id)
    #                     all_edges.add(edge_id)
    #                     collect_descendants(child_id, current_depth + 1)
    #
    #     for node_id in current_nodes:
    #         collect_descendants(node_id, 1)
    #
    #     self.query.create_view(nodes_ids = all_descendants,
    #                           edges_ids = all_edges,
    #                           operation = 'to_descendants',
    #                           params    = {'max_depth': max_depth})
    #     return self
    #
    # def to_ancestors(self, max_depth: Optional[int] = None) -> 'MGraph__Query__Navigate':
    #     """Navigate to all ancestors (parent, grandparent, etc.) up to max_depth."""
    #     current_nodes, _ = self.query.get_current_ids()
    #     all_ancestors = set()
    #     all_edges = set()
    #
    #     def collect_ancestors(node_id: Obj_Id, current_depth: int):
    #         if max_depth is not None and current_depth > max_depth:
    #             return
    #
    #         incoming_edges = self.query.mgraph_index.edges_ids__to__node_id(node_id)
    #         for edge_id in incoming_edges:
    #             edge = self.query.mgraph_data.edge(edge_id)
    #             if edge:
    #                 parent_id = edge.from_node_id()
    #                 if parent_id not in all_ancestors:
    #                     all_ancestors.add(parent_id)
    #                     all_edges.add(edge_id)
    #                     collect_ancestors(parent_id, current_depth + 1)
    #
    #     for node_id in current_nodes:
    #         collect_ancestors(node_id, 1)
    #
    #     self.query.create_view(nodes_ids = all_ancestors,
    #                           edges_ids = all_edges,
    #                           operation = 'to_ancestors',
    #                           params    = {'max_depth': max_depth})
    #     return self