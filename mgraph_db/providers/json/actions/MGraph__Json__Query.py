from typing                                                             import Dict, Any, Union, Set
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node         import Domain__MGraph__Json__Node
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__List   import Domain__MGraph__Json__Node__List
from mgraph_db.query.MGraph__Query                                      import MGraph__Query
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id


class MGraph__Json__Query(MGraph__Query):

    def __getitem__(self, key: Union[str, int]) -> 'MGraph__Json__Query':           # todo: check this method workflow
        if isinstance(key, int):
            return self.get_array_item(key)
        return self.get_dict_item(str(key))

    def get_array_item(self, index: int) -> 'MGraph__Json__Query':                  # todo: check this method workflow
        nodes_ids, _ = self.get_current_ids()
        if not nodes_ids:
            return self.create_empty_view()

        node = self.mgraph_data.node(next(iter(nodes_ids)))
        if not isinstance(node, Domain__MGraph__Json__Node__List):
            return self.create_empty_view()

        items = node.items()
        if not (0 <= index < len(items)):
            return self.create_empty_view()

        item = items[index]
        if isinstance(item, Domain__MGraph__Json__Node):
            return self.with_new_view({item.node_id}, 'array_access', {'index': index})

        return self.create_empty_view()

    def get_dict_item(self, key: str) -> 'MGraph__Json__Query':                         # this method needs refactoring into smaller logical steps and parts
        nodes_ids, _ = self.get_current_ids()
        if not nodes_ids:
            return self.create_empty_view()

        matched_properties = self.mgraph_index.get_nodes_by_field('name', key)          # Find all property nodes with this key


        connecting_edges = set()                                                        # Get all edges connecting our current nodes to these properties
        target_nodes     = set()

        for node_id in nodes_ids:
            edges = self.mgraph_index.get_node_outgoing_edges(self.mgraph_data.node(node_id))
            for edge_id in edges:
                edge = self.mgraph_data.edge(edge_id)
                if edge.to_node_id() in matched_properties:
                    connecting_edges.add(edge_id)
                    value_edges = self.mgraph_index.get_node_outgoing_edges(self.mgraph_data.node(edge.to_node_id()))   # Also get the value nodes connected to these properties
                    connecting_edges.update(value_edges)
                    for value_edge in value_edges:
                        target_nodes.add(self.mgraph_data.edge(value_edge).to_node_id())

        if not target_nodes:
            return self.create_empty_view()

        return self.with_new_view(target_nodes, 'dict_access', {'key': key})

    def name(self, property_name: str) -> 'MGraph__Json__Query':
        matching_ids = self.mgraph_index.get_nodes_by_field('name', property_name)
        nodes_ids, _ = self.get_current_ids()

        filtered_nodes = matching_ids & nodes_ids if nodes_ids else matching_ids
        filtered_edges = self.get_connecting_edges(filtered_nodes)

        self.create_view(nodes_ids=filtered_nodes,
                        edges_ids=filtered_edges,
                        operation='name',
                        params={'name': property_name})
        return self

    def create_empty_view(self) -> 'MGraph__Json__Query':
        self.create_view(nodes_ids=set(),
                        edges_ids=set(),
                        operation='empty',
                        params={})
        return self

    def with_new_view(self, nodes    : Set[Node_Id   ],
                            operation: str           ,
                            params   : Dict[str, Any]
                      ) -> 'MGraph__Json__Query':
        edges = self.get_connecting_edges(nodes)
        self.create_view(nodes_ids=nodes,
                        edges_ids=edges,
                        operation=operation,
                        params=params)
        return self

    def field(self, name):
        return self.with_field('name', name)