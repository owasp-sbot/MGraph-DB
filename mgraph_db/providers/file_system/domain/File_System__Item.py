from typing                                                           import List
from osbot_utils.type_safe.type_safe_core.methods.type_safe_property  import set_as_property
from mgraph_db.mgraph.domain.Domain__MGraph__Node                     import Domain__MGraph__Node
from mgraph_db.providers.file_system.models.Model__File_System__Graph import Model__File_System__Graph
from mgraph_db.providers.file_system.models.Model__File_System__Item  import Model__File_System__Item


class File_System__Item(Domain__MGraph__Node):                                                                      # Base domain class for filesystem items
    node : Model__File_System__Item
    graph: Model__File_System__Graph

    # Properties delegated to the Model layer
    folder_name        = set_as_property('item.data', 'folder_name')
    created_at         = set_as_property('item.data', 'created_at' )
    modified_at        = set_as_property('item.data', 'modified_at')

    def path(self) -> List[str]:                                                                        # Get full path
        path_parts = []
        current_id = self.item.node_id
        visited = set()

        while current_id and current_id not in visited:
            visited.add(current_id)
            current_node = self.graph.node(current_id)
            if not current_node:
                break
            path_parts.append(current_node.folder_name)

            # Find parent folder
            parent_edge = None
            for edge in self.graph.edges():
                if edge.to_node_id == current_id:
                    parent_edge = edge
                    break

            current_id = parent_edge.from_node_id if parent_edge else None

        return list(reversed(path_parts))