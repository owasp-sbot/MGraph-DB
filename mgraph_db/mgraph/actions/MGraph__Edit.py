from typing                                                         import Type
from osbot_utils.helpers.timestamp_capture.decorators.timestamp     import timestamp
from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value           import Schema__MGraph__Node__Value
from mgraph_db.mgraph.actions.MGraph__Data                          import MGraph__Data
from mgraph_db.mgraph.index.MGraph__Index                           import MGraph__Index
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                   import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                 import Edge_Path
from mgraph_db.mgraph.schemas.identifiers.Node_Path                 import Node_Path
from osbot_utils.decorators.methods.cache_on_self                   import cache_on_self
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id


class MGraph__Edit(Type_Safe):
    graph    : Domain__MGraph__Graph
    data_type: Type[MGraph__Data]

    def add_node(self, node: Schema__MGraph__Node):
        with self.index() as index:                                     # used context here so that we have an index object in the state before we add a node (or the node data will be loaded twice)
            result = self.graph.add_node(node)                          # Add node to graph
            index.add_node(node)                                        # Add to index
        return result

    def add_edge(self, edge: Schema__MGraph__Edge):
        result = self.graph.add_edge(edge)                               # Add edge to graph
        self.index().add_edge(edge)                                      # Add to index
        return result

    def create_edge(self):
        node_1 = self.new_node()
        node_2 = self.new_node()
        edge_1 = self.connect_nodes(node_1, node_2)
        return dict(node_1 = node_1,
                    node_2 = node_2,
                    edge_1 = edge_1)

    def connect_nodes(self, from_node: Domain__MGraph__Node,
                            to_node  : Domain__MGraph__Node,
                            edge_type: Type[Schema__MGraph__Edge] = None
                       ) -> Domain__MGraph__Edge:
        edge_domain = self.graph.connect_nodes(from_node=from_node, to_node=to_node, edge_type=edge_type)
        edge_model  = edge_domain.edge
        edge_schema = edge_model.data
        self.index().add_edge(edge_schema)
        return edge_domain


    def get_or_create_edge(self, from_node_id : Node_Id                                 ,
                                 to_node_id   : Node_Id                                 ,
                                 edge_type    : Type[Schema__MGraph__Edge] = None,
                                 predicate    : str = None
                            ) -> Domain__MGraph__Edge:


        if edge_type is None:
            edge_type = Schema__MGraph__Edge

        edge_type_name = edge_type.__name__

        with self.index() as index:

            existing_edges = index.nodes_to_outgoing_edges_by_type().get(from_node_id, {}).get(edge_type_name, set())


            if predicate is not None:
                for edge_id in existing_edges:
                    if index.edges_to_nodes().get(edge_id)[1] == to_node_id:
                        edge = self.data().edge(edge_id)
                        if edge:
                            if edge.edge.data.edge_label:
                                if edge.edge.data.edge_label.predicate == predicate:
                                    return edge


            for edge_id in existing_edges:
                if index.edges_to_nodes().get(edge_id)[1] == to_node_id:
                    if predicate is None:
                        return self.data().edge(edge_id)

            return self.new_edge(edge_type    = edge_type    ,
                                 from_node_id = from_node_id ,
                                 to_node_id   = to_node_id   )

    def rebuild_index(self) -> MGraph__Index:                                    # Force rebuild of index, clearing cache
        return self.index().reload(self.graph.model.data)


    #@timestamp(name='new_node (mgraph_edit)')
    def new_node(self, node_path: Node_Path = None, **kwargs):          # Create new node with optional path
        with self.index() as index:
            if node_path:                                               # todo: see if we need to do this, since new_node ctor should pick it up
                kwargs['node_path'] = node_path                         # Pass path to graph.new_node
            node = self.graph.new_node(**kwargs)                        # Create new node
            index.add_node(node.node.data)                              # Add to index
        return node

    def new_edge(self, edge_path: Edge_Path = None, **kwargs) -> Domain__MGraph__Edge:  # Add a new edge with optional path
        if edge_path:
            kwargs['edge_path'] = edge_path                             # Pass path to graph.new_edge
        edge = self.graph.new_edge(**kwargs)                            # Create new edge
        self.index().add_edge(edge.edge.data)                           # Add to index
        return edge

    #@type_safe
    #@timestamp(name='new_value')
    def new_value(self,                                                 # get or create value (since the values have to be unique)
                  value,
                  key                                          = None,
                  node_type: Type[Schema__MGraph__Node__Value] = None,
                  node_path: Node_Path                         = None,
                  **kwargs__new_node                                    # extra values that will be provided to the new_node method (if used). this can be used to provide a node_id value (to make the node_id value deterministic)
             ) -> Domain__MGraph__Node:
        node_id = self.index().values_index.get_node_id_by_value(value_type=type(value), value=str(value), key=key, node_type=node_type)
        if node_id:
            return self.data().node(node_id)
        if node_type is None:
            node_type= Schema__MGraph__Node__Value
        return self.new_node(node_type  = node_type,
                             value_type = type(value),
                             value      = str(value), key=key,
                             node_path  = node_path,
                             **kwargs__new_node)

    # ---- Path update methods ----

    def set_node_path(self, node_id: Node_Id, node_path: Node_Path) -> bool:    # Set or update a node's path
        node = self.data().node(node_id)
        if node:
            old_path = node.node.data.node_path
            if old_path:                                                # Remove from old path index
                self.index().remove_node_path(node.node.data)
            node.node.data.node_path = node_path                        # Update the node's path
            if node_path:                                               # Add to new path index
                self.index().index_node_path(node.node.data)
            return True
        return False

    def set_edge_path(self, edge_id: Edge_Id, edge_path: Edge_Path) -> bool:    # Set or update an edge's path
        edge = self.data().edge(edge_id)
        if edge:
            old_path = edge.edge.data.edge_path
            if old_path:                                                # Remove from old path index
                self.index().remove_edge_path(edge.edge.data)
            edge.edge.data.edge_path = edge_path                        # Update the edge's path
            if edge_path:                                               # Add to new path index
                self.index().index_edge_path(edge.edge.data)
            return True
        return False

    # ---- Deletion methods ----

    def delete_node(self, node_id: Node_Id) -> bool:                     # Remove a node and its connected edges
        node = self.data().node(node_id)
        if node:
            self.index().remove_node(node.node.data)                     # Remove from index first
        return self.graph.delete_node(node_id)

    def delete_edge(self, edge_id: Edge_Id) -> bool:                     # Remove an edge
        edge = self.data().edge(edge_id)
        if edge:
            self.index().remove_edge(edge.edge.data)                     # Remove from index first
        return self.graph.delete_edge(edge_id)

    @cache_on_self
    def data(self):
        return self.data_type(graph=self.graph)

    #@timestamp(name='.index()')
    @cache_on_self
    def index(self) -> MGraph__Index:                                    # Cached access to index
        return self.graph.index()