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
        if self.config.display.edge_type:
            edge_type = edge.edge.data.edge_type
            type_name = self.type_name__from__type(edge_type)
            return [f'label="  {type_name}"']
        elif self.config.display.edge_ids:
            return [f'label="  {edge.edge_id}"']
        return []

    def format_edge_definition(self, source: str, target: str, attrs: List[str]) -> str:
        attrs_str = f' [{", ".join(attrs)}]' if attrs else ''
        return f'  "{source}" -> "{target}"{attrs_str}'
