from typing                                                             import List
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
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id        import Obj_Id
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe



class Model__MGraph__Graph(Type_Safe):
    data       : Schema__MGraph__Graph
    model_types: Model__MGraph__Types

    graph_id = set_as_property('data', 'graph_id', Obj_Id)

    @type_safe
    def add_node(self, node: Schema__MGraph__Node) -> Model__MGraph__Node:                            # Add a node to the graph
        self.data.nodes[node.node_id] = node
        return self.model_types.node_model_type(data=node)

    @type_safe
    def add_edge(self, edge: Schema__MGraph__Edge) -> Model__MGraph__Edge:                            # Add an edge to the graph
        if edge.from_node_id not in self.data.nodes:
            raise ValueError(f"From node {edge.from_node_id} not found")
        if edge.to_node_id not in self.data.nodes:
            raise ValueError(f"To node {edge.to_node_id} not found")

        self.data.edges[edge.edge_id] = edge
        return self.model_types.edge_model_type(data=edge)

    def new_edge(self, **kwargs) -> Model__MGraph__Edge:
        edge_type = self.data.schema_types.edge_type
        edge      = edge_type(**kwargs)
        return self.add_edge(edge)

    def new_node(self, **kwargs):
        if 'node_type' in kwargs and 'node_data' in kwargs:                 # if node_type and node_data is provided, then we have all we need to create the new node
            node_type = kwargs.get('node_type')
            node_data = kwargs.get('node_data')
            del kwargs['node_type']
            del kwargs['node_data']
            node      = node_type(node_data=node_data, **kwargs)
            return self.add_node(node)

        if 'node_type' in kwargs:
            node_type              = kwargs.get('node_type')                                    # if we have the node_type here
            node_type__annotations = dict(type_safe_cache.get_class_annotations(node_type))     # get its annotations
            node_data_type         = node_type__annotations.get('node_data')                    # so that we can resolve the node_data object

        else:
            node_type              = self.data.schema_types.node_type               # Get the node type from the schema
            node_data_type         = self.data.schema_types.node_data_type          # Get the node data type from the schema
            node_type__annotations = dict(type_safe_cache.get_class_annotations(node_type))


        node_type__kwargs           = {}                                # Separate kwargs for node_type and node_data_type
        node_data__type_kwargs      = {}
        node_data_type__annotations = dict(type_safe_cache.get_class_annotations(node_data_type))

        for key, value in kwargs.items():                               # todo: review this 'feature' to split the kwargs based on the node and the data class
            if key in node_type__annotations:                           #       there could be some cases where this is useful (like how it is used in the mermaid provider
                node_type__kwargs[key] = value                          #       but in general this is not a good pattern to follow
            if key in node_data_type__annotations:
                node_data__type_kwargs[key] = value

        if issubclass(node_data_type, Schema__MGraph__Node__Value__Data):       # handle edge case which happens when we are creating a new value node
            if node_data__type_kwargs == {}:                                    # but have not provided any value
                node_data__type_kwargs['key'] = Obj_Id()                        # which means we need to make sure this is an unique node (or it can't be indexed)
        node_data = node_data_type(**node_data__type_kwargs                )    # Create node data object           # todo: see if this is be test way (and location) to handle this

        node      = node_type     (node_data=node_data, **node_type__kwargs)    # Create a node with the node data

        return self.add_node(node)

    def edges(self):
        return [self.model_types.edge_model_type(data=data) for data in self.data.edges.values()]

    def edge(self, edge_id: Obj_Id) -> Model__MGraph__Edge:
        data = self.data.edges.get(edge_id)
        if data:
            return self.model_types.edge_model_type(data=data)

    def edges_ids(self):
        return list(self.data.edges.keys())

    def graph(self):
        return self.data

    def node(self, node_id: Obj_Id) -> Model__MGraph__Node:
        data = self.data.nodes.get(node_id)
        if data:
            return self.model_types.node_model_type(data=data)

    def node__from_edges(self, node_id) -> List[Model__MGraph__Edge]:                             # Get model edges where this node is the source
        outgoing_edges = []
        for edge in self.edges():
            if edge.from_node_id() == node_id:
                outgoing_edges.append(edge)
        return outgoing_edges

    def node__to_edges(self, node_id) -> List[Model__MGraph__Edge]:                             # Get model edges where this node is the source
        incoming_edges = []
        for edge in self.edges():
            if edge.to_node_id() == node_id:
                incoming_edges.append(edge)
        return incoming_edges

    def nodes(self) -> List[Model__MGraph__Node]:
        return [self.model_types.node_model_type(data=node) for node in self.data.nodes.values()]

    def nodes_ids(self):
        return list(self.data.nodes.keys())

    @type_safe
    def delete_node(self, node_id: Obj_Id) -> 'Model__MGraph__Graph':                              # Remove a node and all its connected edges
        if node_id not in self.data.nodes:
            return False

        edges_to_remove = []                                                                            # Remove all edges connected to this node
        for edge_id, edge in self.data.edges.items():
            if edge.from_node_id == node_id or edge.to_node_id == node_id:
                edges_to_remove.append(edge_id)

        for edge_id in edges_to_remove:
            del self.data.edges[edge_id]

        del self.data.nodes[node_id]
        return True

    @type_safe
    def delete_edge(self, edge_id: Obj_Id) -> 'Model__MGraph__Graph':                              # Remove an edge from the graph
        if edge_id not in self.data.edges:
            return False

        del self.data.edges[edge_id]
        return True