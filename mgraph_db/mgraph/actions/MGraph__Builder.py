from typing                                                 import List, Optional, Type, Any, Union
from mgraph_db.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_db.mgraph.domain.Domain__MGraph__Edge           import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Node           import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from mgraph_db.mgraph.actions.MGraph__Edit                  import MGraph__Edit
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Label   import Schema__MGraph__Edge__Label
from osbot_utils.helpers.Obj_Id                             import Obj_Id
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

# todo: move the data fields into a new class Schema__MGraph__Builder__Data

class MGraph__Builder(Type_Safe):
    mgraph_edit             : MGraph__Edit                                # Reference to the MGraph__Edit instance
    config__unique_values   : bool = False
    node__current           : Domain__MGraph__Node        = None          # Current active node
    node__history           : List[Domain__MGraph__Node]                  # History of visited nodes
    edge__current           : Domain__MGraph__Edge        = None          # Current active edge
    edge__history           : List[Domain__MGraph__Edge]                  # History of created edges
    node__root              : Domain__MGraph__Node        = None          # Root node of the current build

    # Node Operations -------------------------------------------------------

    def add_connected_node(self, value                                  ,
                                 edge_type : Optional[Type[Schema__MGraph__Edge]] = None,
                                 predicate : Optional[str]                        = None,
                                 node_type : Optional[Type[Schema__MGraph__Node]] = None,
                                 **kwargs
                          ) -> 'MGraph__Builder':                                          # Add a new node connected to the current one

        if not self.node__current:
            raise ValueError("No current node set. Use add_node() or set_current_node() first.")

        if self.config__unique_values:                                              # Create the new node
            kwargs['key'] = Obj_Id()

        node_kwargs = kwargs.copy()                                                 # Use node_type if provided, otherwise default behavior
        if node_type:
            node_kwargs['node_type'] = node_type


        previous_current = self.node__current                                       # Create the new node without changing the current context
        new_node = self.mgraph_edit.new_value(value, **node_kwargs)

        self.node__current = previous_current                                       # Re-establish the previous current node (since new_value may have changed it)

        if predicate:                                                               # Use existing add_predicate method to connect with predicate
            return self.add_predicate(predicate = predicate,
                                      target    = new_node,
                                      edge_type = edge_type)
        else:
            edge = self.mgraph_edit.connect_nodes(from_node = self.node__current,       # Create standard connection
                                                  to_node   = new_node,
                                                  edge_type = edge_type)

            return self.register_edge(edge, new_node)


    def add_node(self, value, **kwargs) -> 'MGraph__Builder':   # Add a new value node and make it the current context.
        if self.config__unique_values:
            kwargs['key'] = Obj_Id()
        node = self.mgraph_edit.new_value(value, **kwargs)
        return self.register_node(node)

    def graph(self):
        return self.node__current.graph

    def new_node(self, **kwargs) -> 'MGraph__Builder':          # Add a new node (non-value) and make it the current context.
        node = self.mgraph_edit.new_node(**kwargs)
        return self.register_node(node)

    def node_id(self):
        return self.current_node().node_id

    def set_current_node(self, node_or_id: Union[Domain__MGraph__Node, Obj_Id]) -> 'MGraph__Builder':           # Set the current node context by node object or ID."""
        if isinstance(node_or_id, Domain__MGraph__Node):
            node = node_or_id
        else:
            node = self.mgraph_edit.data().node(node_or_id)

        if not node:
            raise ValueError(f"Node with ID {node_or_id} not found")

        return self.register_node(node)

    # Edge Operations -------------------------------------------------------
    # todo add support for connecting using edge's predicate and labels
    def connect_to(self, target, edge_type: Type[Schema__MGraph__Edge] = None, **kwargs) -> 'MGraph__Builder':  # Connect the current node to another node.
        if not self.node__current:
            raise ValueError("No current node set. Use add_node() or set_current_node() first.")

        if isinstance(target, Domain__MGraph__Node):
            target_node = target
        elif isinstance(target, Obj_Id):
            target_node = self.mgraph_edit.data().node(target)
            if not target_node:
                raise ValueError(f"Node with ID {target} not found")
        else:
            target_node = self.mgraph_edit.new_value(target, **kwargs)              # If target is a value, create a new node for it

        edge = self.mgraph_edit.connect_nodes(from_node = self.node__current,       # Create edge between current node and target
                                              to_node   = target_node       ,
                                              edge_type = edge_type         )

        return self.register_edge(edge, target_node)

    def register_edge(self, edge, to_node) -> None:                      # Internal helper to update node context and history.
        self.edge__history.append(edge)
        self.edge__current = edge
        self.register_node(to_node)
        return self

    def register_node(self, node) -> None:                      # Internal helper to update node context and history.
        if not self.node__root:
            self.node__root = node

        self.node__current = node
        self.node__history.append(node)

        return self

    # todo: refactor with connect_to and add support for outgoing and incomming label
    def add_predicate(self, predicate: str                              ,
                            target   : Any                              ,
                            edge_type: Type[Schema__MGraph__Edge] = None,
                            node_type: Type[Schema__MGraph__Node] = None,
                            **kwargs) -> 'MGraph__Builder':  # Add a semantic relationship with a predicate between the current node and target."""
        if not self.node__current:
            raise ValueError("No current node set. Use add_node() or set_current() first.")

        target_node = None
        if isinstance(target, Domain__MGraph__Node):                                    # check if target is a node already
            target_node = target
        elif isinstance(target, Obj_Id):                                                # if target is an Obj_Id, see if points to an existing node (and if so used it)
            obj_id_node = self.mgraph_edit.data().node(target)
            if obj_id_node:
                target_node =  obj_id_node
        if not target_node:                                                             # else use target as value node
            if self.config__unique_values:
                kwargs['key'] = Obj_Id()
            target_node = self.mgraph_edit.new_value(target, node_type=node_type, **kwargs)


        domain_edge = self.mgraph_edit.get_or_create_edge(edge_type    = edge_type                 ,
                                                          from_node_id = self.node__current.node_id,             # Create edge between current node and target
                                                          to_node_id   = target_node       .node_id)

        edge_data   = domain_edge.edge.data
        edge_label  = Schema__MGraph__Edge__Label(predicate=Safe_Id(predicate), outgoing=Safe_Id(predicate))
        edge_data.edge_label = edge_label                                               # todo refactor this to use a helper method to set an edge label's value

        return self.register_edge(domain_edge, target_node)


    # Navigation Operations -------------------------------------------------

    def node_up(self) -> 'MGraph__Builder':                             # Navigate up to the previous node in history.
        if len(self.node__history) >= 2:                                # Pop the current node (which is at the top of the history)
            self.node__history.pop()
            self.node__current = self.node__history[-1]                 # Now the top of history is the previous node, so assign it to current
        elif len(self.node__history) == 1:                              # Special case: only one item in history, pop it but don't change current
            self.node__history.pop()
            self.node__current = self.node__root
        return self

    def edge_up(self) -> 'MGraph__Builder':                             # Navigate to the previous edge in history.
        if self.edge__history:
            self.edge__current = self.edge__history.pop()
        return self

    def root(self) -> 'MGraph__Builder':                                # Return to the root node of the current build.
        if self.node__root:
            if self.node__current and self.node__current.node_id != self.node__root.node_id:
                self.node__history.append(self.node__current)
            self.node__current = self.node__root
        return self

    def up(self):
        return self.node_up()

    # Utility Methods -------------------------------------------------------

    def current_node(self) -> Optional[Domain__MGraph__Node]:                               # Get the current node.
        return self.node__current

    def current_edge(self) -> Optional[Domain__MGraph__Edge]:                               # Get the current edge.
        return self.edge__current

    def root_node(self) -> Optional[Domain__MGraph__Node]:                                  # Get the root node of the current build.
        return self.node__root