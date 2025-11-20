from typing                                                           import Type, Tuple, Optional, Any
from mgraph_db.mgraph.actions.MGraph__Edit                            import MGraph__Edit
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                     import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Node                     import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                    import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value             import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data       import Schema__MGraph__Node__Value__Data
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe


class MGraph__Values(Type_Safe):
    mgraph_edit: MGraph__Edit                                                                            # Reference to edit capabilities

    def get_by_hash(self, value_hash: str) -> Optional[Domain__MGraph__Node]:
        node_id = self.mgraph_edit.index().values_index.get_node_id_by_hash(value_hash)
        if node_id:
            return self.mgraph_edit.data().node(node_id)
        return None

    def get_by_value(self, value_type: Type, value: str) -> Optional[Domain__MGraph__Node]:
        node_id = self.mgraph_edit.index().values_index.get_node_id_by_value(value_type, value)
        if node_id:
            return self.mgraph_edit.data().node(node_id)
        return None

    def get_or_create(self, value: Any, key:str='') -> Optional[Domain__MGraph__Node]:

        node_id = self.mgraph_edit.index().values_index.get_node_id_by_value(value_type=type(value), value=str(value), key=key)                   # First try to find existing value node
        if node_id:
            return self.mgraph_edit.data().node(node_id)

        node_value_data = Schema__MGraph__Node__Value__Data(value= str(value),value_type=type(value), key=key)              # Create new if not found
        node_value      = Schema__MGraph__Node__Value      (node_data = node_value_data                      )
        new_node        = self.mgraph_edit.add_node        (node_value                                       )
        return new_node

    def get_or_create_value(self, value    : Any                        ,
                                  edge_type: Type [Schema__MGraph__Edge],
                                  from_node: Domain__MGraph__Node
                            ) -> Tuple[Domain__MGraph__Node, Domain__MGraph__Edge]:
        value_node = self.get_or_create(value)
        if value_node is None:
            raise ValueError(f"Unsupported value type: {type(value)}")

        # Check for existing edge of this type from the source node
        existing_edges = self.mgraph_edit.index().nodes_to_outgoing_edges_by_type().get(from_node.node_id, {}).get(
            edge_type.__name__, set())
        for edge_id in existing_edges:
            edge = self.mgraph_edit.data().edge(edge_id)
            if edge and edge.to_node_id() == value_node.node_id:
                return value_node, edge

        edge = self.mgraph_edit.new_edge(edge_type    = edge_type         ,
                                         from_node_id = from_node.node_id ,
                                         to_node_id   = value_node.node_id)

        return value_node, edge

    def get_linked_value(self, from_node : Domain__MGraph__Node       ,                                # Get value through edge type
                               edge_type : Type[Schema__MGraph__Edge]
                          ) -> Optional[Domain__MGraph__Node]:

        connected_node_id = self.mgraph_edit.index().get_node_connected_to_node__outgoing(node_id   = from_node.node_id,
                                                                                          edge_type = edge_type.__name__)
        if connected_node_id:
            return self.mgraph_edit.data().node(connected_node_id)
        return None
