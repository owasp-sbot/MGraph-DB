from typing                                                                  import List
from mgraph_db.mgraph.actions.exporters.dot.render.MGraph__Export__Dot__Base import MGraph__Export__Dot__Base
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                            import Domain__MGraph__Edge


class MGraph__Export__Dot__Edge__Renderer(MGraph__Export__Dot__Base):

    def create_edge_attributes(self, edge: Domain__MGraph__Edge) -> List[str]:
        return (self.create_edge_base_attributes  (edge) +
                self.create_edge_style_attributes (edge) +
                self.create_edge_label_attributes (edge))

    def create_edge_base_attributes(self, edge: Domain__MGraph__Edge) -> List[str]:
        attrs = []
        edge_type = edge.edge.data.edge_type

        if edge_type in self.config.type.edge_color:
            attrs.append(f'color="{self.config.type.edge_color[edge_type]}"')
        return attrs

    def create_edge_style_attributes(self, edge: Domain__MGraph__Edge) -> List[str]:
        attrs = []
        edge_type = edge.edge.data.edge_type

        if edge_type in self.config.type.edge_style:
            attrs.append(f'style="{self.config.type.edge_style[edge_type]}"')
        return attrs

    def create_edge_label_attributes(self, edge: Domain__MGraph__Edge) -> List[str]:
        label_parts = []
        if self.config.display.edge_id:
            label_parts.append(f"  edge_id = '{edge.edge_id}'")
        if self.config.display.edge_type:
            edge_type = edge.edge.data.edge_type
            type_name = self.type_name__from__type(edge_type)
            label_parts.append(f"  edge_type = '{type_name}'")
        if self.config.display.edge_type_str:                                       # todo: review this use of _str to create an entry with no label
            edge_type = edge.edge.data.edge_type
            type_name = self.type_name__from__type(edge_type)
            label_parts.append(f"{type_name}")
        if self.config.display.edge_type_full_name:
            type_full_name = edge.edge.data.edge_type.__name__
            label_parts.append(f"  edge_type_full_name = '{type_full_name}'")

        if self.config.display.edge_predicate:
            if edge.edge.data.edge_label:
                label_part = edge.edge.data.edge_label.predicate                    # todo: (with with what happens in the node rendered) refactor out this logic (since it is repeated multiple times and we are reusing a local variable)
                if self.config.render.label_show_var_name:
                    label_part = f"predicate='{label_part}'"
                label_parts.append(label_part)

        if self.config.display.edge_predicate_str:
            if edge.edge.data.edge_label:
                label_parts.append(f"{edge.edge.data.edge_label.predicate}")

        if label_parts:  # Combine all parts
            if len(label_parts) == 1:
                return [f'label="{label_parts[0]}"']
            else:
                return [f'label="{"\\l".join(label_parts)}\\l"']
        return label_parts

    def format_edge_definition(self, source: str, target: str, attrs: List[str]) -> str:
        attrs_str = f' [{", ".join(attrs)}]' if attrs else ''
        return f'  "{source}" -> "{target}"{attrs_str}'
