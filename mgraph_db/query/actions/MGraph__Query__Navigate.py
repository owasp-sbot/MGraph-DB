from typing                                          import Type, Optional
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