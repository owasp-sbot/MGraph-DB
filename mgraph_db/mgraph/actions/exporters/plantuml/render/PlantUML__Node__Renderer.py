from typing                                                                     import Optional
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from mgraph_db.mgraph.domain.Domain__MGraph__Node                               import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                        import Schema__MGraph__Node__Data
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config        import PlantUML__Config
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Base          import PlantUML__Base


class PlantUML__Node__Renderer(PlantUML__Base):                                       # renders a single node to PlantUML statement
    config               : PlantUML__Config                   = None                  # rendering configuration

    def render(self, node: Domain__MGraph__Node,                                      # render node to complete statement
                     node_data: Schema__MGraph__Node__Data) -> str:
        puml_id    = self.safe_id(node.node_id)                                       # sanitized PlantUML ID
        label      = self.build_label(node, node_data)                                # build display label
        shape      = self.config.node.shape                                           # get shape from config
        color      = self.resolve_color(node)                                         # resolve background color

        if color:                                                                     # build statement with color
            return f'{shape} "{label}" as {puml_id} #{color}'
        return f'{shape} "{label}" as {puml_id}'                                      # build statement without color

    def build_label(self, node: Domain__MGraph__Node,                                 # build node display label
                          node_data: Schema__MGraph__Node__Data) -> str:
        parts      = []                                                               # label parts
        display    = self.config.display                                              # display settings

        if display.show_node_type:                                                    # add type name
            type_name = self.type_name__from__type(node.node_type)
            parts.append(f'<<{type_name}>>')

        if display.show_node_value:                                                   # add value if present
            value = self.extract_value(node_data)
            if value is not None:
                wrapped = self.wrap_text(str(value), display.wrap_at)
                parts.append(wrapped)

        if display.show_node_id:                                                      # add node ID
            node_id_str = str(node.node_id)[:8]
            parts.append(f'[{node_id_str}]')

        if not parts:                                                                 # fallback to type name
            type_name = self.type_name__from__type(node.node_type)
            parts.append(str(type_name))

        label = '\\n'.join(parts)                                                     # join with PlantUML newlines
        return self.escape_label(label)

    def resolve_color(self, node: Domain__MGraph__Node) -> Optional[Safe_Str__Id]:    # resolve node color
        type_name  = str(self.type_name__from__type(node.node_type))
        type_colors = self.config.node.type_colors or {}

        if type_name in type_colors:                                                  # check type mapping
            return type_colors[type_name]

        return self.config.node.default_color                                         # use default

    def extract_value(self, node_data: Schema__MGraph__Node__Data):                   # extract value from node data
        if node_data and hasattr(node_data, 'value'):
            return node_data.value
        return None
