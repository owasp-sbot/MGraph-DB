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
        edge_type = self.resolver.edge_type(edge.edge.data.edge_type)                       # Resolve type using resolver

        if edge_type in self.config.type.edge_color:
            attrs.append(f'color="{self.config.type.edge_color[edge_type]}"')
        return attrs

    def create_edge_style_attributes(self, edge: Domain__MGraph__Edge) -> List[str]:
        attrs = []
        edge_type = self.resolver.edge_type(edge.edge.data.edge_type)                       # Resolve type using resolver

        if edge_type in self.config.type.edge_style:
            attrs.append(f'style="{self.config.type.edge_style[edge_type]}"')
        return attrs

    def create_edge_label_attributes(self, edge: Domain__MGraph__Edge) -> List[str]:
        label_parts = []
        if self.config.display.edge_id_str:
            label_parts.append(f'{edge.edge_id}')
        elif self.config.display.edge_id:
            label_parts.append(f"  edge_id = '{edge.edge_id}'")
        if self.config.display.edge_path_str:
            label_parts.append(f'{edge.edge.data.edge_path}')
        elif self.config.display.edge_path:
            label_parts.append(f"  edge_path = '{edge.edge.data.edge_path}'")
        if self.config.display.edge_type:
            edge_type = self.resolver.edge_type(edge.edge.data.edge_type)                   # Resolve type using resolver
            type_name = self.type_name__from__type(edge_type)
            label_parts.append(f"  edge_type = '{type_name}'")
        if self.config.display.edge_type_str:                                               # todo: review this use of _str to create an entry with no label
            edge_type = self.resolver.edge_type(edge.edge.data.edge_type)                   # Resolve type using resolver
            type_name = self.type_name__from__type(edge_type)
            label_parts.append(f"{type_name}")
        if self.config.display.edge_type_full_name:
            edge_type = self.resolver.edge_type(edge.edge.data.edge_type)                   # Resolve type using resolver
            type_full_name = edge_type.__name__
            label_parts.append(f"  edge_type_full_name = '{type_full_name}'")

        if self.config.display.edge_predicate_str:
            if edge.edge.data.edge_label:
                label_parts.append(f"{edge.edge.data.edge_label.predicate}")
        elif self.config.display.edge_predicate:
            if edge.edge.data.edge_label:
                label_part = edge.edge.data.edge_label.predicate                            # todo: (with with what happens in the node rendered) refactor out this logic (since it is repeated multiple times and we are reusing a local variable)
                label_part = f"  predicate='{label_part}'"
                label_parts.append(label_part)


        if label_parts:                                                                     # Combine all parts
            if len(label_parts) == 1:
                return [f'label="{label_parts[0]}"']
            else:
                return [f'label="{"\\l".join(label_parts)}\\l"']
        return label_parts

    def format_edge_definition(self, source: str, target: str, attrs: List[str]) -> str:
        attrs_str = f' [{", ".join(attrs)}]' if attrs else ''
        return f'  "{source}" -> "{target}"{attrs_str}'