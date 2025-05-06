from typing                                          import Set, Optional, Dict, Any, Type

from mgraph_db.mgraph.schemas.Schema__MGraph__Node import Schema__MGraph__Node

from mgraph_db.mgraph.schemas.Schema__MGraph__Edge   import Schema__MGraph__Edge
from mgraph_db.query.domain.Domain__MGraph__Query    import Domain__MGraph__Query
from osbot_utils.helpers.Obj_Id                      import Obj_Id
from osbot_utils.type_safe.Type_Safe                 import Type_Safe


class MGraph__Query__Add(Type_Safe):
    query: Domain__MGraph__Query                                                    # Reference to domain query

    def add_node_id(self, node_id: Obj_Id) -> 'MGraph__Query__Add':               # Add specific node to view
        if not self.query.mgraph_data.node(node_id):                              # Validate node exists
            return self

        return self.new_view(additional_nodes = {node_id},
                             operation        = 'add_node_id',
                             params           = {'node_id': str(node_id)})

    # def add_nodes_ids(self, nodes_ids: Set[Obj_Id]) -> 'MGraph__Query__Add':
    #     valid_nodes = {node_id for node_id in nodes_ids
    #                    if self.query.mgraph_data.node(node_id)}
    #
    #     if not valid_nodes:
    #         return self
    #     params = {'nodes_ids': [str(node_id) for node_id in valid_nodes]}
    #     return self.new_view(additional_nodes = valid_nodes    ,
    #                          operation        = 'add_nodes_ids',
    #                          params           = params         )

    def add_nodes_ids(self, nodes_ids: Set[Obj_Id]) -> 'MGraph__Query__Add':  # Add multiple nodes to view
        current_nodes, current_edges = self.query.get_current_ids()  # Get current nodes and edges

        # Filter out any invalid node IDs
        valid_nodes = {node_id for node_id in nodes_ids
                       if self.query.mgraph_data.node(node_id)}  # Validate nodes exist

        if not valid_nodes:  # Return if no valid nodes
            return self

        new_nodes = current_nodes | valid_nodes  # Add new nodes to set
        new_edges = current_edges  # Start with current edges

        self.query.create_view(nodes_ids=new_nodes,
                         edges_ids=new_edges,
                         operation='add_nodes_ids',
                         params={'nodes_ids': [str(node_id) for node_id in
                                               valid_nodes]})  # Create new view with added nodes
        return self

    def add_node_with_value(self, value: any) -> 'MGraph__Query__Add':
        matching_id = self.find_value_node(value)
        if not matching_id:
            return self

        value_node = {matching_id}

        params = {'value_type': type(value).__name__, 'value'     : str(value)}
        return self.new_view(additional_nodes = value_node          ,
                             operation       = 'add_node_with_value',
                             params          = params               )

    def add_nodes_with_incoming_edge(self, edge_type: Type[Schema__MGraph__Edge]) -> 'MGraph__Query__Add':  # Add nodes that have incoming edges of specific type
        current_nodes, _ = self.query.get_current_ids()
        target_edges     = self.query.mgraph_index.get_edges_by_type(edge_type)                             # Get all edges of this type
        new_nodes        = set()

        for edge_id in target_edges:                                                                        # For each matching edge
            edge = self.query.mgraph_data.edge(edge_id)
            if edge and edge.to_node_id() in current_nodes:                                                 # If target node is in current view
                source_node = edge.from_node_id()
                if source_node not in current_nodes:                                                        # Only add if not already in view
                    new_nodes.add(source_node)

        if not new_nodes:                                                                                   # If no new nodes to add
            return self

        return self.new_view(additional_nodes=new_nodes,
                             operation='add_nodes_with_incoming_edge',
                             params={'edge_type': edge_type.__name__})

    def add_nodes_with_outgoing_edge(self, edge_type: Type[Schema__MGraph__Edge], connect_edges=True) -> 'MGraph__Query__Add':  # Add nodes that have outgoing edges of specific type
        current_nodes, _ = self.query.get_current_ids()
        target_edges     = self.query.mgraph_index.get_edges_by_type(edge_type)                             # Get all edges of this type
        new_nodes        = set()
        new_edges        = set()
        for edge_id in target_edges:                                                                        # For each matching edge
            edge = self.query.mgraph_data.edge(edge_id)
            if edge:
                target_node = edge.to_node_id()
                if target_node not in current_nodes:                                                        # Only add if not already in view
                    new_nodes.add(target_node)
                    if connect_edges and edge.from_node_id() in current_nodes:
                        new_edges.add(edge.edge_id)

        if not new_nodes:                                                                                   # If no new nodes to add
            return self                                                                                     # just return

        return self.new_view(additional_nodes = new_nodes,
                             additional_edges = new_edges,
                             operation='add_nodes_with_outgoing_edge',
                             params={'edge_type': edge_type.__name__})

    def add_nodes_with_type(self, node_type: Type[Schema__MGraph__Node]):
        nodes_ids = self.query.mgraph_index.get_nodes_by_type(node_type)
        if nodes_ids:
            self.add_nodes_ids(nodes_ids)
        return self

    # todo: review the name of this since this more like the expand_graph logic
    def add_outgoing_edges(self, depth: Optional[int] = None) -> 'MGraph__Query__Add':    # Add outgoing edges
        if depth is not None and depth <= 0:
            return self

        current_nodes, current_edges = self.query.get_current_ids()             # Get current state
        new_nodes = set()                                                       # Initialize new sets
        new_edges = set()

        for node_id in current_nodes:                                          # Process each current node
            node = self.query.mgraph_data.node(node_id)
            if node:
                outgoing_edges = self.query.mgraph_index.get_node_outgoing_edges(node)
                new_edges.update(outgoing_edges)

                for edge_id in outgoing_edges:                                 # Add target nodes
                    edge = self.query.mgraph_data.edge(edge_id)
                    if edge:
                        new_nodes.add(edge.to_node_id())

        if new_nodes or new_edges:      # stop when there are no more new edges of nodes
            combined_nodes = current_nodes | new_nodes                             # Combine sets
            combined_edges = current_edges | new_edges

            self.query.create_view(nodes_ids = combined_nodes,
                                  edges_ids = combined_edges,
                                  operation = 'add_outgoing_edges',
                                  params    = {'depth': depth})

            if depth is not None:                                                 # Recursive case for depth
                return self.add_outgoing_edges(depth - 1)

        return self

    def find_value_node(self, value: any) -> Optional[Obj_Id]:
        return self.query.mgraph_index.values_index.get_node_id_by_value(type(value),str(value))

    # todo: refactor out from this add class
    def new_view(self, additional_nodes: Set[Obj_Id]   = None,
                       additional_edges: Set[Obj_Id]   = None,
                       operation       : str           = None,
                       params          : Dict[str, Any]= None
                 ) -> 'MGraph__Query__Add':
        current_nodes, current_edges = self.query.get_current_ids()             # get current nodes and edges ids
        new_nodes = current_nodes | (additional_nodes or set())                            # merge sets
        new_edges = current_edges | (additional_edges or set())                           # merge sets

        self.query.create_view(nodes_ids = new_nodes ,
                               edges_ids  = new_edges,
                               operation  = operation or 'NA',
                               params     = params    or {} )
        return self
