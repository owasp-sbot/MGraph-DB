from typing                                                 import Dict, Type, Set
from mgraph_db.mgraph.MGraph                                import MGraph
from mgraph_db.mgraph.schemas.Schema__MGraph__Diff__Values  import Schema__MGraph__Diff__Values
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

class MGraph__Diff__Values(Type_Safe):
    graph1 : MGraph
    graph2 : MGraph

    def get_values_by_type(self, mgraph, value_type: Type) -> Dict[str, str]:               # Get all values of a specific type using the values index
        values = {}
        with mgraph.edit() as edit:
            with edit.index() as index:                                                     # Use MGraph__Values to handle value nodes
                nodes = index.values_index.index_data.values_by_type.get(value_type, set()) # Get nodes for this value type
                for value_hash in nodes:
                    node_id = index.values_index.get_node_id_by_hash(value_hash)
                    if node_id:
                        node = mgraph.data().node(node_id)
                        if node and node.node_data:
                            key = node.node_data.key or str(value_hash)                     # Use key if available, fallback to hash
                            values[key] = node.node_data.value
        return values

    def get_connected_values(self, mgraph, value: str, edge_type: Type[Schema__MGraph__Edge]) -> Set[str]:  # Get all values connected to a specific value through an edge type
        connected_values = set()
        with mgraph.edit() as edit:
            with edit.index() as index:
                node_id = index.values_index.get_node_id_by_value(edge_type, value)                                             # Find value node
                if node_id:
                    outgoing_edges = index.nodes_to_outgoing_edges_by_type().get(node_id, {}).get(edge_type.__name__, set())    # Get edges of specified type
                    for edge_id in outgoing_edges:
                        to_node_id = index.edges_to_nodes()[edge_id][1]
                        to_node = mgraph.data().node(to_node_id)
                        if to_node and to_node.node_data:
                            connected_values.add(to_node.node_data.value)
        return connected_values

    def compare(self, value_types: list[Type]) -> Schema__MGraph__Diff__Values:                 # Compare graphs based on specified value types
        value_diff = Schema__MGraph__Diff__Values()

        for value_type in value_types:                                                          # Compare values for each type
            values1     = self.get_values_by_type(self.graph1, value_type)
            values2     = self.get_values_by_type(self.graph2, value_type)
            values1_set = set(values1.values())                                                 # Find added and removed values
            values2_set = set(values2.values())

            if values1_set - values2_set:
                value_diff.added_values  [value_type] = values1_set - values2_set
            if values2_set - values1_set:
                value_diff.removed_values[value_type] = values2_set - values1_set

            # todo see if need this changed_relationships diff
            #common_values = values1_set & values2_set                               # Find common values to check their relationships

            # for value in common_values:                                             # Compare relationships for common values
            #     edge_types = self.get_edge_types_for_value(value_type)              # Get edge types for this value type
            #
            #     for edge_type in edge_types:
            #         connected1 = self.get_connected_values(self.graph1, value, edge_type)
            #         connected2 = self.get_connected_values(self.graph2, value, edge_type)
            #
            #         if connected1 != connected2:
            #             if value not in value_diff.changed_relationships:
            #                 value_diff.changed_relationships[value] = {}
            #             value_diff.changed_relationships[value][edge_type] = connected1 ^ connected2  # Symmetric difference

        return value_diff


    # def get_edge_types_for_value(self, value_type: Type) -> list[Type[Schema__MGraph__Edge]]:
    #     """Get relevant edge types for a value type"""
    #     # This should be overridden by specific implementations to return
    #     # the relevant edge types for each value type
    #    return []