from typing                                                     import Dict, Any, List, Optional, Set
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Base    import MGraph__Export__Base
from mgraph_db.mgraph.domain.Domain__MGraph__Node               import Domain__MGraph__Node
from osbot_utils.helpers.Obj_Id                                 import Obj_Id
from osbot_utils.type_safe.decorators.type_safe                 import type_safe

class MGraph__Export__Tree_Values(MGraph__Export__Base):
    max_depth          : int = 5                                                                # Maximum recursion depth   # todo: see impact of this
    max_children       : int = 20                                                               # Maximum children per node # todo: see impact of this
    root_nodes_ids     : List[Obj_Id]                                                           # IDs of the root nodes
    visited_nodes      : Set[Obj_Id]                                                            # Track visited nodes to prevent cycles

    def create_node_data(self, node: Domain__MGraph__Node) -> Dict[str, Any]:                   # Create node data for tree export
        node_id = str(node.node_id)
        node_value = None

        if hasattr(node.node_data, 'value'):                                                    # Extract node value if it exists
            node_value = node.node_data.value

                    # todo: change these to a Type_Safe class
        node_data = {'id'       : node_id       ,                                               # Create basic node representation
                     'value'    : str(node_value) if node_value is not None else node_id,
                     'children' : {}            }                                               # Group children by edge predicate

        return node_data

    def build_tree_structure(self, node_id: Obj_Id, depth: int = 0) -> Optional[Dict[str, Any]]:    # Build a hierarchical tree structure starting from a node
        if depth >= self.max_depth or node_id in self.visited_nodes:                                # Check for max depth or cycle
            return None

        self.visited_nodes.add(node_id)                                                             # Mark as visited to prevent cycles

        node = self.graph.node(node_id)                                                             # Get node
        if not node:
            return None

        node_data = self.create_node_data(node)                                                     # Get node data

        outgoing_edges = self.graph.model.node__from_edges(node_id)                                 # Process outgoing edges
        child_count = 0

        for edge in outgoing_edges:
            if child_count >= self.max_children:                                                    # todo: see impact of this (at least log when it happens)
                break

            predicate = "connects_to"                                                               # Default predicate (relationship type)

            if hasattr(edge.data, 'edge_label') and edge.data.edge_label:                           # Try to get edge label if available
                if hasattr(edge.data.edge_label, 'predicate') and edge.data.edge_label.predicate:
                    predicate = str(edge.data.edge_label.predicate)
                elif hasattr(edge.data.edge_label, 'outgoing') and edge.data.edge_label.outgoing:
                    predicate = str(edge.data.edge_label.outgoing)

            target_id   = edge.to_node_id()                                                         # Get target node
            target_node = self.graph.node(target_id)

            if target_node:
                if predicate not in node_data['children']:                                          # Initialize the predicate entry if it doesn't exist
                    node_data['children'][predicate] = []

                if hasattr(target_node.node_data, 'value'):                                         # Get target node value
                    target_value = str(target_node.node_data.value)
                else:
                    target_value = str(target_id)

                if target_id not in self.visited_nodes:                                             # Process target node recursively if not too deep
                    child_tree = self.build_tree_structure(target_id, depth + 1)
                    if child_tree:
                        node_data['children'][predicate].append(child_tree)
                        child_count += 1
                else:                                                                               # If already visited, just add reference without recursing
                                                            # todo: change these to a Type_Safe class
                    node_data['children'][predicate].append({'id'      : str(target_id),
                                                             'value'   : target_value  ,
                                                             'children': {}            ,            # Empty children to indicate this is a reference
                                                             'recursive': True         })           # Todo: see if this is the best way to handle this

        return node_data

    @type_safe
    def format_output(self) -> Dict[str, Any]:                                                      # Format the processed data as a tree structure
        self.visited_nodes = set()                                                                  # Reset visited nodes for each run

        trees = []
        for node_id in self.root_nodes_ids:
            tree = self.build_tree_structure(node_id)
            if tree:
                trees.append(tree)

        return { 'trees': trees }                                                                   # todo: change to a Type_Safe class

    def format_as_text(self, tree: Dict[str, Any], indent: int = 0) -> str:                         # Format the tree as text with indentation
        if not tree:
            return ""

        result = [" " * indent + tree['value']]

        for predicate, children in tree['children'].items():
            result.append(" " * (indent + 4) + predicate + ":")
            for child in children:
                result.append(self.format_as_text(child, indent + 8))

        return "\n".join(result)

    def as_text(self, root_nodes_ids: List[Obj_Id]) -> str:
        self.root_nodes_ids = root_nodes_ids
        tree_as_text = ""
        for tree in self.format_output().get('trees'):
            tree_as_text += self.format_as_text(tree)
            tree_as_text += "\n\n--------\n\n"
        return tree_as_text

    def print_as_text(self, root_nodes_ids: List[Obj_Id]):
        print(root_nodes_ids)
        as_text = self.as_text(root_nodes_ids)
        print()
        print(as_text)
        return as_text