from mgraph_db.mgraph.MGraph                                import MGraph
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Diff__Values  import Schema__MGraph__Diff__Values
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

class Edge__Diff__Added   (Schema__MGraph__Edge): pass                                    # Edge type for added values
class Edge__Diff__Removed (Schema__MGraph__Edge): pass                                    # Edge type for removed values
class Edge__Diff__Type    (Schema__MGraph__Edge): pass                                    # Edge type for type connections

class MGraph__View__Diff__Values(Type_Safe):
    diff   : Schema__MGraph__Diff__Values                                                # The diff to visualize
    mgraph : MGraph                                                                      # The graph we create

    def create_graph(self) -> MGraph:                                                   # Create graph visualization
        with self.mgraph.edit() as edit:
            center = edit.new_value('Graph Diff (on Values)')                           # Create center node
            added_node   = edit.new_value('Added'  )                                        # Create added/removed parent nodes
            removed_node = edit.new_value('Removed')

            edit.new_edge(from_node_id = center.node_id,                                # Connect center to sections with type edges
                          to_node_id   = added_node.node_id,
                          edge_type    = Edge__Diff__Type)
            edit.new_edge(from_node_id = center.node_id,
                          to_node_id   = removed_node.node_id,
                          edge_type    = Edge__Diff__Type)

            # Handle added values
            for value_type in self.diff.added_values.keys():
                value_type_name = value_type.__name__
                value_type_key  = f'added_{value_type_name}'                            # make sure this is unique, or we will get mixed results (where the same type has added and removed items)
                type_node = edit.new_value(value_type_name, key=value_type_key)                            # Create type node under "Added"
                edit.new_edge(from_node_id = added_node.node_id,                       # Connect with added edge type
                              to_node_id   = type_node.node_id,
                              edge_type    = Edge__Diff__Added)

                for value in self.diff.added_values[value_type]:                       # Create value nodes
                    value_node = edit.new_value(value)
                    edit.new_edge(from_node_id = type_node.node_id,                    # Connect values with added edge type
                                  to_node_id   = value_node.node_id,
                                  edge_type    = Edge__Diff__Added)

            # Handle removed values
            for value_type in self.diff.removed_values.keys():
                value_type_name = value_type.__name__
                type_node = edit.new_value(value_type_name)                            # Create type node under "Removed"
                edit.new_edge(from_node_id = removed_node.node_id,                     # Connect with removed edge type
                              to_node_id   = type_node.node_id,
                              edge_type    = Edge__Diff__Removed)

                for value in self.diff.removed_values[value_type]:                     # Create value nodes
                    value_node = edit.new_value(value)
                    edit.new_edge(from_node_id = type_node.node_id,                    # Connect values with removed edge type
                                  to_node_id   = value_node.node_id,
                                  edge_type    = Edge__Diff__Removed)
        return self.mgraph

    def create_mgraph_screenshot(self):                                                # Configure DOT visualization settings
        with self.mgraph.screenshot() as _:
            with _.export().export_dot() as dot:

                dot.show_node__value()                                                   # Show node values

                dot.set_graph__layout_engine__dot()
                dot.set_graph__rank_dir__lr()                                         # Top to bottom layout



                # Edge styling
                dot.set_edge__arrow_head__vee()  # Arrow styling

                color__type    = "#F0FFFF"
                color__added   = "#98FB98"
                color__removed = "#FFB6C6"

                #dot.set_edge__type_color(Edge__Diff__Type   , color__type   )             # Gray for type edges
                dot.set_edge__type_color(Edge__Diff__Added  , color__added  )             # Green for added
                dot.set_edge__type_color(Edge__Diff__Removed, color__removed)             # Red for removed

                # Node styling
                dot.set_node__shape__type__box()                                        # Box shape for nodes
                dot.set_node__shape__rounded()                                          # With rounded corners
                dot.set_node__fill_color("#E8E8E8")                                     # Light gray background
                dot.set_edge_to_node__type_fill_color(Edge__Diff__Added  , color__added  )
                dot.set_edge_to_node__type_fill_color(Edge__Diff__Removed, color__removed)
                dot.set_edge_to_node__type_fill_color(Edge__Diff__Type   , color__type   )


            return _