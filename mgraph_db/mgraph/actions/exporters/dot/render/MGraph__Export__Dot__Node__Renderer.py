from typing                                                                  import List
from mgraph_db.mgraph.actions.exporters.dot.render.MGraph__Export__Dot__Base import MGraph__Export__Dot__Base
from mgraph_db.mgraph.domain.Domain__MGraph__Node                            import Domain__MGraph__Node


class MGraph__Export__Dot__Node__Renderer(MGraph__Export__Dot__Base):

    def create_node_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        return (self.create_node_base_attributes   (node) +
                self.create_node_shape_attributes  (node) +                         # todo: change how this works since this is not a good way to return the attributes
                self.create_node_font_attributes   (node) +
                self.create_node_style_attributes  (node) +                         # todo:        since for example both create_node_shape_attributes can create an style attribute
                self.create_node_label_attributes  (node))

    def create_node_base_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        return []                                                                # Base implementation

    def create_node_shape_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        attrs = {}
        styles = set()
        node_type = node.node.data.node_type

        # Start with base node configuration
        if self.config.node.shape.type       : attrs['shape'    ] = f'shape="{self.config.node.shape.type}"'
        if self.config.node.shape.width      : attrs['width'    ] = f'width={self.config.node.shape.width}'
        if self.config.node.shape.height     : attrs['height'   ] = f'height={self.config.node.shape.height}'
        if self.config.node.shape.fixed_size : attrs['fixedsize'] = 'true'
        if self.config.node.shape.rounded    : styles.add('rounded')
        if self.config.node.shape.fill_color:
            styles.add('filled')
            attrs['fillcolor'] = f'fillcolor="{self.config.node.shape.fill_color}"'

        # Apply type-specific shape configuration
        if node_type in self.config.type.shapes:
            shape_config = self.config.type.shapes[node_type]
            if shape_config.type:       attrs['shape'] = f'shape="{shape_config.type}"'
            if shape_config.width:      attrs['width'] = f'width={shape_config.width}'
            if shape_config.height:     attrs['height'] = f'height={shape_config.height}'
            if shape_config.fixed_size: attrs['fixedsize'] = 'true'
            if shape_config.fill_color:
                styles.add('filled')
                attrs['fillcolor'] = f'fillcolor="{shape_config.fill_color}"'

        # Then apply value_type specific configuration if this is a value node
        if hasattr(node.node_data, 'value_type'):
            value_type = node.node_data.value_type
            if value_type in self.config.type.value_shapes:
                shape_config = self.config.type.value_shapes[value_type]
                if shape_config.type:       attrs['shape'] = f'shape="{shape_config.type}"'
                if shape_config.width:      attrs['width'] = f'width={shape_config.width}'
                if shape_config.height:     attrs['height'] = f'height={shape_config.height}'
                if shape_config.fixed_size: attrs['fixedsize'] = 'true'
                if shape_config.fill_color:
                    styles.add('filled')
                    attrs['fillcolor'] = f'fillcolor="{shape_config.fill_color}"'
                if shape_config.rounded:    styles.add('rounded')
                if shape_config.style:      styles.update(shape_config.style.split(','))


        # Check edges where this node is the source
        for edge in self.graph.model.node__from_edges(node.node_id):
            edge_type = edge.data.edge_type
            if edge_type in self.config.type.edge_from:
                shape = self.config.type.edge_from[edge_type].shapes
                if shape.type:
                    attrs['shape'] = f'shape="{shape.type}"'
                if shape.fill_color:
                    styles.add('filled')
                    attrs['fillcolor'] = f'fillcolor="{shape.fill_color}"'

        # Check edges where this node is the target
        for edge in self.graph.model.node__to_edges(node.node_id):
            edge_type = edge.data.edge_type
            if edge_type in self.config.type.edge_to:
                shape = self.config.type.edge_to[edge_type].shapes
                if shape.type:       attrs['shape'] = f'shape="{shape.type}"'
                if shape.fill_color:
                    styles.add('filled')
                    attrs['fillcolor'] = f'fillcolor="{shape.fill_color}"'

        # Add style attribute if we have any styles
        if styles:
            attrs['style'] = f'style="{",".join(sorted(styles))}"'

        return list(attrs.values())

    def create_node_font_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        attrs = {}                                                                          # Use dict to prevent duplicates
        node_type = node.node.data.node_type

        # Apply type-specific font configuration first (base styling)
        if node_type in self.config.type.fonts:
            font_config = self.config.type.fonts[node_type]
            if font_config.name:  attrs['fontname'] = f'fontname="{font_config.name}"'
            if font_config.size:  attrs['fontsize'] = f'fontsize="{font_config.size}"'
            if font_config.color: attrs['fontcolor'] = f'fontcolor="{font_config.color}"'

        # Then apply value_type specific configuration if this is a value node
        if hasattr(node.node_data, 'value_type'):
            value_type = node.node_data.value_type
            if value_type in self.config.type.value_fonts:
                font_config = self.config.type.value_fonts[value_type]
                if font_config.name:  attrs['fontname'] = f'fontname="{font_config.name}"'
                if font_config.size:  attrs['fontsize'] = f'fontsize="{font_config.size}"'
                if font_config.color: attrs['fontcolor'] = f'fontcolor="{font_config.color}"'

        # Check edges where this node is the source
        for edge in self.graph.model.node__from_edges(node.node_id):
            edge_type = edge.data.edge_type
            if edge_type in self.config.type.edge_from:
                font = self.config.type.edge_from[edge_type].fonts
                if font.name:  attrs['fontname'] = f'fontname="{font.name}"'
                if font.size:  attrs['fontsize'] = f'fontsize="{font.size}"'
                if font.color: attrs['fontcolor'] = f'fontcolor="{font.color}"'

        # Check edges where this node is the target
        for edge in self.graph.model.node__to_edges(node.node_id):
            edge_type = edge.data.edge_type
            if edge_type in self.config.type.edge_to:
                font = self.config.type.edge_to[edge_type].fonts
                if font.name:  attrs['fontname'] = f'fontname="{font.name}"'
                if font.size:  attrs['fontsize'] = f'fontsize="{font.size}"'
                if font.color: attrs['fontcolor'] = f'fontcolor="{font.color}"'

        return list(attrs.values())

    def create_node_style_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        styles = set()
        node_type = node.node.data.node_type

        if node_type in self.config.type.shapes:
            shape_config = self.config.type.shapes[node_type]
            if shape_config.fill_color: styles.add('filled')
            if shape_config.rounded:    styles.add('rounded')
            if shape_config.style:      styles.update(shape_config.style.split(','))

        # Add value_type styles if applicable
        if hasattr(node.node_data, 'value_type'):
            value_type = node.node_data.value_type
            if value_type in self.config.type.value_shapes:
                shape_config = self.config.type.value_shapes[value_type]
                if shape_config.fill_color: styles.add('filled')
                if shape_config.rounded:    styles.add('rounded')
                if shape_config.style:      styles.update(shape_config.style.split(','))

        return [f'style="{",".join(sorted(styles))}"'] if styles else []

    def create_node_label_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        label_parts = []
        if self.config.display.node_id:                                                       # Add node_id if requested
            label_part = node.node_id                                                        # todo: refactor out this logic (since it is repeated multiple times and we are reusing a local variable)
            if self.config.render.label_show_var_name:
                label_part = f"node_id='{label_part}'"
            label_parts.append(label_part)
        if self.config.display.node_type:
            node_type = node.node.data.node_type
            type_name = self.type_name__from__type(node_type)
            label_part = type_name
            if self.config.render.label_show_var_name:
                label_part = f"node_type='{label_part}'"
            label_parts.append(label_part)
        if self.config.display.node_type_full_name:
            type_full_name = node.node.data.node_type.__name__
            label_parts.append(f"node_type_full_name='{type_full_name}'")
        if hasattr(node.node_data, 'value'):                                                  # Only proceed for nodes with value data
            #if self.config.display.node_value_str:                                                # Add value if requested
            #    label_parts.append(f"{node.node_data.value}")
            if self.config.display.node_value:                                                # Add value if requested
                label_part = node.node_data.value                                             # todo: refactor out this logic (since it is repeated multiple times and we are reusing a local variable)
                if self.config.render.label_show_var_name:
                    label_part = f"node_value='{label_part}'"
                label_parts.append(label_part)
            if self.config.display.node_value_type:                                           # Add value_type if requested
                type_name = self.type_name__from__type(node.node_data.value_type)
                label_parts.append(f"node_value_type='{type_name}'")
            if self.config.display.node_value_key:                                            # Add key if requested
                label_part = node.node_data.key                                             # todo: refactor out this logic (since it is repeated multiple times and we are reusing a local variable)
                if self.config.render.label_show_var_name:
                    label_part = f"node_value_key='{label_part}'"
                label_parts.append(label_part)
        if label_parts:  # Combine all parts
            if len(label_parts)==1:
                return [f'label="{label_parts[0]}"']
            else:
                return [f'label="{"\\l".join(label_parts)}\\l"']
        return []

    def format_node_definition(self, node_id: str, attrs: List[str]) -> str:
        attrs_str = f' [{", ".join(attrs)}]' if attrs else ''
        return f'  "{node_id}"{attrs_str}'