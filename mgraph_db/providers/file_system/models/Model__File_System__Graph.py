from mgraph_db.mgraph.models.Model__MGraph__Graph                             import Model__MGraph__Graph
from mgraph_db.providers.file_system.models.Model__File_System__Default_Types import Model__File_System__Default_Types
from mgraph_db.providers.file_system.schemas.Schema__File_System__Graph       import Schema__File_System__Graph
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id             import Node_Id


class Model__File_System__Graph(Model__MGraph__Graph):                                                   # Model for filesystem graph
    data          : Schema__File_System__Graph
    model_types   : Model__File_System__Default_Types


    def allow_circular_refs(self) -> bool:                                                               # Check if circular refs allowed
        return self.data.graph_data.allow_circular_refs

    def set_allow_circular_refs(self, value: bool) -> 'Model__File_System__Graph':                      # Set circular refs policy
        self.data.graph_data.allow_circular_refs = value
        return self

    # todo: check the logic of this method, since the from_node_id is not used inside it
    def validate_no_cycles(self, from_node_id: Node_Id, to_node_id: Node_Id) -> bool:           # Validate no circular refs
        if self.allow_circular_refs():
            return True

        visited = set()
        def has_cycle(current_id: Node_Id) -> bool:
            if current_id in visited:
                return True
            visited.add(current_id)
            for edge in self.data.edges.values():
                if edge.from_node_id == current_id:
                    if has_cycle(edge.to_node_id):
                        return True
            visited.remove(current_id)
            return False

        return not has_cycle(to_node_id)

    def add_edge(self, edge):                                                                           # Override to check cycles
        if not self.validate_no_cycles(edge.from_node_id, edge.to_node_id):
            raise ValueError("Adding this edge would create a cycle")
        return super().add_edge(edge)