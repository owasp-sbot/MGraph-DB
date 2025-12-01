from mgraph_db.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                   import Domain__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Diff                  import Schema__MGraph__Diff, Schema__MGraph__Node__Changes, Schema__MGraph__Change__Data, Schema__MGraph__Change__Type, Schema__MGraph__Edge__Changes, Schema__MGraph__Change__Node
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id


class MGraph__Diff(Type_Safe):
    graph_a: Domain__MGraph__Graph
    graph_b: Domain__MGraph__Graph

    def diff_graphs(self) -> Schema__MGraph__Diff:
        """Compare two graphs and return detailed statistics about their differences"""
        nodes_a = set(self.graph_a.nodes_ids())
        nodes_b = set(self.graph_b.nodes_ids())
        edges_a = set(self.graph_a.edges_ids())
        edges_b = set(self.graph_b.edges_ids())

        nodes_added   = nodes_b - nodes_a
        nodes_removed = nodes_a - nodes_b
        edges_added   = edges_b - edges_a
        edges_removed = edges_a - edges_b

        nodes_modified = {}
        nodes_common = nodes_a & nodes_b
        for node_id in nodes_common:
            changes = self.compare_node_data(node_id)
            # Only add to nodes_modified if there are actual changes
            if changes.data is not None or changes.type is not None:
                nodes_modified[node_id] = changes

        edges_modified = {}
        edges_common = edges_a & edges_b
        for edge_id in edges_common:
            edge_a = self.graph_a.edge(edge_id)
            edge_b = self.graph_b.edge(edge_id)
            if not self.edges_equal(edge_a, edge_b):
                edges_modified[edge_id] = self.compare_edge_data(edge_id)

        return Schema__MGraph__Diff(
            nodes_added      = sorted(nodes_added),
            nodes_removed    = sorted(nodes_removed),
            nodes_modified   = nodes_modified,
            edges_added      = sorted(edges_added),
            edges_removed    = sorted(edges_removed),
            edges_modified   = edges_modified,
            nodes_count_diff = len(nodes_b) - len(nodes_a),
            edges_count_diff = len(edges_b) - len(edges_a)
        )

    def compare_node_data(self, node_id: Node_Id) -> Schema__MGraph__Node__Changes:
        """Compare data for a specific node between the two graphs"""
        node_a = self.graph_a.node(node_id)
        node_b = self.graph_b.node(node_id)

        if not node_a or not node_b:
            return Schema__MGraph__Node__Changes()

        changes = Schema__MGraph__Node__Changes()

        # Compare node data and only set if there are actual differences
        if node_a.node_data != node_b.node_data:
            data_a = node_a.node_data.json() if node_a.node_data else {}
            data_b = node_b.node_data.json() if node_b.node_data else {}

            # Compare field by field and only include changed values
            changed_fields_a = {}
            changed_fields_b = {}

            for key in data_a.keys() | data_b.keys():  # Union of all keys
                value_a = data_a.get(key)
                value_b = data_b.get(key)
                if value_a != value_b:
                    if key in data_a: changed_fields_a[key] = value_a
                    if key in data_b: changed_fields_b[key] = value_b

            # Only create change data if there are actual differences
            if changed_fields_a or changed_fields_b:
                changes.data = Schema__MGraph__Change__Data(
                    from_value = changed_fields_a,
                    to_value   = changed_fields_b
                )

        # Compare node types and only set if different
        if node_a.node_type != node_b.node_type:
            changes.type = Schema__MGraph__Change__Type(
                from_value = node_a.node_type,
                to_value   = node_b.node_type
            )

        return changes

    def compare_edge_data(self, edge_id: Edge_Id) -> Schema__MGraph__Edge__Changes:
        """Compare data for a specific edge between the two graphs"""
        edge_a = self.graph_a.edge(edge_id)
        edge_b = self.graph_b.edge(edge_id)

        if not edge_a or not edge_b:
            return Schema__MGraph__Edge__Changes()

        changes = Schema__MGraph__Edge__Changes()

        # Compare edge types and only set if different
        if edge_a.edge.data.edge_type != edge_b.edge.data.edge_type:
            changes.type = Schema__MGraph__Change__Type(
                from_value = edge_a.edge.data.edge_type,
                to_value   = edge_b.edge.data.edge_type
            )

        # Compare from_node and only set if different
        if edge_a.from_node_id() != edge_b.from_node_id():
            changes.from_node = Schema__MGraph__Change__Node(
                from_value = edge_a.from_node_id(),
                to_value   = edge_b.from_node_id()
            )

        # Compare to_node and only set if different
        if edge_a.to_node_id() != edge_b.to_node_id():
            changes.to_node = Schema__MGraph__Change__Node(
                from_value = edge_a.to_node_id(),
                to_value   = edge_b.to_node_id()
            )

        return changes

    def nodes_equal(self, node_a: Domain__MGraph__Node, node_b: Domain__MGraph__Node) -> bool:
        """Compare two nodes for equality"""
        if not node_a or not node_b:
            return False

        return (node_a.node_type == node_b.node_type and
                node_a.node_data == node_b.node_data)

    def edges_equal(self, edge_a: Domain__MGraph__Edge, edge_b: Domain__MGraph__Edge) -> bool:
        """Compare two edges for equality"""
        if not edge_a or not edge_b:
            return False

        return (edge_a.edge.data.edge_type == edge_b.edge.data.edge_type and
                edge_a.from_node_id() == edge_b.from_node_id() and
                edge_a.to_node_id() == edge_b.to_node_id())