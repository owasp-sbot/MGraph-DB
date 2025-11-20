from typing                                                                  import Dict, Any, List
from mgraph_db.mgraph.actions.exporters.dot.render.MGraph__Export__Dot__Base import MGraph__Export__Dot__Base


class MGraph__Export__Dot__Format__Generator(MGraph__Export__Dot__Base):

    def generate_graph_header(self) -> List[str]:                                # Generate DOT header with all global settings
        lines = ['digraph {']

        # Graph attributes
        graph_attrs = []
        if self.config.graph.background_color : graph_attrs.append(f'bgcolor="{self.config.graph.background_color}"')
        if self.config.graph.layout_engine    : graph_attrs.append(f'layout="{self.config.graph.layout_engine}"'    )
        if self.config.graph.overlap          : graph_attrs.append(f'overlap="{self.config.graph.overlap}"'         )
        if self.config.graph.margin           : graph_attrs.append(f'margin="{self.config.graph.margin}"'           )
        if self.config.graph.rank_dir         : graph_attrs.append(f'rankdir="{self.config.graph.rank_dir}"'        )
        if self.config.graph.rank_sep         : graph_attrs.append(f'ranksep={self.config.graph.rank_sep}'          )
        if self.config.graph.node_sep         : graph_attrs.append(f'nodesep={self.config.graph.node_sep}'          )
        if self.config.graph.splines          : graph_attrs.append(f'splines="{self.config.graph.splines}"'         )
        if self.config.graph.epsilon          : graph_attrs.append(f'epsilon="{self.config.graph.epsilon}"'         )
        if self.config.graph.spring_constant  : graph_attrs.append(f'K="{self.config.graph.spring_constant}"'       )

        if self.config.graph.title            : graph_attrs.append(f'label="\\n{self.config.graph.title}\\n\\n" labelloc="t"') # adds label to the top (with a new line before and after)
        if self.config.graph.title__font.size : graph_attrs.append(f'fontsize="{ self.config.graph.title__font.size}"' )
        if self.config.graph.title__font.color: graph_attrs.append(f'fontcolor="{self.config.graph.title__font.color}"')
        if self.config.graph.title__font.name : graph_attrs.append(f'fontname="{ self.config.graph.title__font.name}"' )


        if graph_attrs:
            lines.append(f'  graph [{", ".join(graph_attrs)}]')

        # Global node settings
        node_attrs = []
        node_styles = set()

        if self.config.node.font.name : node_attrs.append(f'fontname="{self.config.node.font.name}"'  )
        if self.config.node.font.size : node_attrs.append(f'fontsize="{self.config.node.font.size}"'  )
        if self.config.node.font.color: node_attrs.append(f'fontcolor="{self.config.node.font.color}"')
        if self.config.node.shape.type: node_attrs.append(f'shape="{self.config.node.shape.type}"'    )

        if self.config.node.shape.fill_color:                                                 # Handle fill color
            node_attrs.append(f'fillcolor="{self.config.node.shape.fill_color}"')
            node_styles.add('filled')

        if self.config.node.shape.rounded: node_styles.add('rounded')                        # Additional styles
        if self.config.node.shape.style:   node_styles.update(self.config.node.shape.style.split(','))

        if node_styles:                                                                      # Combine all styles
            node_attrs.append(f'style="{",".join(sorted(node_styles))}"')

        if node_attrs:
            lines.append(f'  node [{", ".join(node_attrs)}]')

        # Global edge settings
        edge_attrs = []
        if self.config.edge.arrow_head: edge_attrs.append(f'arrowhead="{self.config.edge.arrow_head}"')
        if self.config.edge.arrow_size: edge_attrs.append(f'arrowsize="{self.config.edge.arrow_size}"')
        if self.config.edge.color     : edge_attrs.append(f'color="{self.config.edge.color}"'         )
        if self.config.edge.font.name : edge_attrs.append(f'fontname="{self.config.edge.font.name}"'  )
        if self.config.edge.font.size : edge_attrs.append(f'fontsize="{self.config.edge.font.size}"'  )
        if self.config.edge.font.color: edge_attrs.append(f'fontcolor="{self.config.edge.font.color}"')

        if edge_attrs:
            lines.append(f'  edge [{", ".join(edge_attrs)}]')

        return lines

    def format_attributes(self, attrs: Dict[str, Any]) -> str:                   # Format attributes for DOT
        formatted = []
        for key, value in attrs.items():
            if isinstance(value, str):
                formatted.append(f'{key}="{value}"')
            else:
                formatted.append(f'{key}={value}')
        return ", ".join(formatted)

    def escape_string(self, value: str) -> str:                                  # Escape special characters
        return value.replace('"', '\\"').replace('\n', '\\n')