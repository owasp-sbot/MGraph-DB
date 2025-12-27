from typing                                                             import List
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                import Schema__MGraph__Node__Data
from osbot_utils.helpers.timestamp_capture.decorators.timestamp         import timestamp
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id        import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id       import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id       import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id      import Graph_Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe          import type_safe
from osbot_utils.type_safe.type_safe_core.methods.type_safe_property    import set_as_property
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Cache       import type_safe_cache
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data         import Schema__MGraph__Node__Value__Data
from mgraph_db.mgraph.models.Model__MGraph__Types                       import Model__MGraph__Types
from mgraph_db.mgraph.models.Model__MGraph__Edge                        import Model__MGraph__Edge
from mgraph_db.mgraph.models.Model__MGraph__Node                        import Model__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                     import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                      import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                      import Schema__MGraph__Edge
from mgraph_db.mgraph.actions.MGraph__Type__Resolver                    import MGraph__Type__Resolver
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe



class Model__MGraph__Graph(Type_Safe):
    data       : Schema__MGraph__Graph
    model_types: Model__MGraph__Types
    resolver   : MGraph__Type__Resolver                                                     # Auto-instantiated - provides type resolution

    graph_id = set_as_property('data', 'graph_id', Graph_Id)

    @type_safe
    def add_node(self, node: Schema__MGraph__Node) -> Model__MGraph__Node:                  # Add a node to the graph
        self.data.nodes[node.node_id] = node
        type_value                    = self.model_types.node_model_type if self.model_types else None
        node_model_type               = self.resolver.node_model_type(type_value)
        return node_model_type(data=node)

    @type_safe
    def add_edge(self, edge: Schema__MGraph__Edge) -> Model__MGraph__Edge:                  # Add an edge to the graph
        if edge.from_node_id not in self.data.nodes:
            raise ValueError(f"From node {edge.from_node_id} not found")
        if edge.to_node_id not in self.data.nodes:
            raise ValueError(f"To node {edge.to_node_id} not found")

        self.data.edges[edge.edge_id] = edge
        edge_model_type = self.resolver.edge_model_type(
            self.model_types.edge_model_type if self.model_types else None
        )
        return edge_model_type(data=edge)

    def new_edge(self, **kwargs) -> Model__MGraph__Edge:
        if kwargs.get('edge_type') is None :
            if self.data.schema_types is not None:                                          # Check for schema_types
                edge_type = self.data.schema_types.edge_type
                edge_type = self.resolver.edge_type(edge_type)                              # Resolve if None
            elif self.model_types.edge_model_type:
                edge_type = self.model_types.edge_model_type.__annotations__.get('data')
            else:                                                                           # Fallback to defaults
                edge_type = self.resolver.edge_type(None)
            kwargs['edge_type'] = edge_type


        edge = kwargs.get('edge_type')(**kwargs)
        return self.add_edge(edge)

    @timestamp(name='new_node (model_mgraph)')
    def new_node(self, **kwargs):
        if 'node_type' in kwargs and 'node_data' in kwargs:                                 # if node_type and node_data is provided, then we have all we need to create the new node
            node_type = kwargs.get('node_type')
            node_data = kwargs.get('node_data')
            #del kwargs['node_type']
            del kwargs['node_data']
            node      = node_type(node_data=node_data, **kwargs)
            return self.add_node(node)

        add_node_type_to_node = False
        if 'node_type' in kwargs:
            node_type              = kwargs.get('node_type')                                # if we have the node_type here
            node_type__annotations = dict(type_safe_cache.get_class_annotations(node_type)) # get its annotations
            node_data_type         = node_type__annotations.get('node_data')                # so that we can resolve the node_data object
        elif self.data.schema_types is not None:                                            # Check for schema_types
            node_type      = self.data.schema_types.node_type
            node_data_type = self.data.schema_types.node_data_type
            node_type      = self.resolver.node_type(node_type)                             # Resolve if None
            node_data_type = self.resolver.node_data_type(node_data_type)                   # Resolve if None
            node_type__annotations = dict(type_safe_cache.get_class_annotations(node_type))
            add_node_type_to_node = True
        elif self.model_types.node_model_type:
            node_type = self.model_types.node_model_type.__annotations__.get('data')
            node_type__annotations = dict(type_safe_cache.get_class_annotations(node_type)) # get its annotations
            node_data_type         = node_type__annotations.get('node_data')                # so that we can resolve the node_data object
            add_node_type_to_node = True
        else:                                                                               # Fallback to defaults
            node_type      = self.resolver.node_type(None)
            node_data_type = self.resolver.node_data_type(None)
            node_type__annotations = dict(type_safe_cache.get_class_annotations(node_type))


        node_type__kwargs           = {}                                                    # Separate kwargs for node_type and node_data_type
        node_data__type_kwargs      = {}
        node_data_type__annotations = dict(type_safe_cache.get_class_annotations(node_data_type))

        for key, value in kwargs.items():                                                   # todo: review this 'feature' to split the kwargs based on the node and the data class
            if key in node_type__annotations:                                               #       there could be some cases where this is useful (like how it is used in the mermaid provider
                node_type__kwargs[key] = value                                              #       but in general this is not a good pattern to follow
            if key in node_data_type__annotations:
                node_data__type_kwargs[key] = value
        if node_data_type is Schema__MGraph__Node__Data:                                    # if this is a Schema__MGraph__Node__Data
            node_data = None                                                                # then we don't need to create the object since Schema__MGraph__Node__Data has not attributes
        else:
            if issubclass(node_data_type, Schema__MGraph__Node__Value__Data):                   # handle edge case which happens when we are creating a new value node
                if node_data__type_kwargs == {}:                                                # but have not provided any value
                    node_data__type_kwargs['key'] = Node_Id(Node_Id(Obj_Id()))                  # which means we need to make sure this is an unique node (or it can't be indexed)
            node_data = node_data_type(**node_data__type_kwargs                )                # Create node data object           # todo: see if this is be test way (and location) to handle this

        node      = node_type     (node_data=node_data, **node_type__kwargs)                # Create a node with the node data

        if add_node_type_to_node:                                                          # if this is set, it means that we are not using the defaults (or None value)
            node.node_type = node_type                                                     #   which means that we need to set this value

        return self.add_node(node)

    def edges(self):
        edge_model_type = self.resolver.edge_model_type(
            self.model_types.edge_model_type if self.model_types else None
        )
        return [edge_model_type(data=data) for data in self.data.edges.values()]

    def edge(self, edge_id: Edge_Id) -> Model__MGraph__Edge:
        data = self.data.edges.get(edge_id)
        if data:
            edge_model_type = self.resolver.edge_model_type(
                self.model_types.edge_model_type if self.model_types else None
            )
            return edge_model_type(data=data)
        return None

    def edges_ids(self):
        return list(self.data.edges.keys())

    def graph(self):
        return self.data

    def node(self, node_id: Node_Id) -> Model__MGraph__Node:
        data = self.data.nodes.get(node_id)
        if data:
            node_model_type = self.resolver.node_model_type(
                self.model_types.node_model_type if self.model_types else None
            )
            return node_model_type(data=data)

    def node__from_edges(self, node_id) -> List[Model__MGraph__Edge]:                       # Get model edges where this node is the source
        outgoing_edges = []
        for edge in self.edges():
            if edge.from_node_id() == node_id:
                outgoing_edges.append(edge)
        return outgoing_edges

    def node__to_edges(self, node_id) -> List[Model__MGraph__Edge]:                         # Get model edges where this node is the source
        incoming_edges = []
        for edge in self.edges():
            if edge.to_node_id() == node_id:
                incoming_edges.append(edge)
        return incoming_edges

    def nodes(self) -> List[Model__MGraph__Node]:
        node_model_type = self.resolver.node_model_type(
            self.model_types.node_model_type if self.model_types else None
        )
        return [node_model_type(data=node) for node in self.data.nodes.values()]

    def nodes_ids(self):
        return list(self.data.nodes.keys())

    @type_safe
    def delete_node(self, node_id: Node_Id) -> bool:                                        # Remove a node and all its connected edges
        if node_id not in self.data.nodes:
            return False

        edges_to_remove = []                                                                # Remove all edges connected to this node
        for edge_id, edge in self.data.edges.items():
            if edge.from_node_id == node_id or edge.to_node_id == node_id:
                edges_to_remove.append(edge_id)

        for edge_id in edges_to_remove:
            del self.data.edges[edge_id]

        del self.data.nodes[node_id]
        return True

    @type_safe
    def delete_edge(self, edge_id: Edge_Id) -> bool:                                        # Remove an edge from the graph
        if edge_id not in self.data.edges:
            return False

        del self.data.edges[edge_id]
        return True