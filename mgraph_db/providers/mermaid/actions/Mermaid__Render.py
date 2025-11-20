from typing                                                                 import List
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Render__Config    import Schema__Mermaid__Render__Config
from osbot_utils.type_safe.type_safe_core.methods.type_safe_property        import set_as_property
from osbot_utils.utils.Str                                                  import safe_str
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Node               import LINE_PADDING, Domain__Mermaid__Node
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Graph              import Domain__Mermaid__Graph
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe


class Mermaid__Render(Type_Safe):
    graph         : Domain__Mermaid__Graph
    mermaid_code  : List
    render_config = set_as_property('graph.model.data', 'render_config', Schema__Mermaid__Render__Config)

    def add_line(self, line:str) -> str:
        self.mermaid_code.append(line)
        return line

    def code(self) -> str:
        self.code_create()
        return '\n'.join(self.mermaid_code)

    def code_create(self, recreate=False):
        with self as _:
            if recreate:                            # if recreate is True, reset the code
                _.reset_code()
            elif self.mermaid_code:                 # if the code has already been created, don't create it
                return self                         #   todo: find a better way to do this, namely around the concept of auto detecting (on change) when the recreation needs to be done (vs being able to use the previously calculated data)
            for directive in _.render_config.directives:
                _.add_line(f'%%{{{directive}}}%%')
            _.add_line(self.graph_header())
            if self.render_config.add_nodes:
                for node in self.graph.nodes():
                    node_code = self.render_node(node)
                    _.add_line(node_code)
            if self.render_config.line_before_edges:
                _.add_line('')
            for edge in self.graph.edges():
                edge_code = self.render_edge(edge)
                _.add_line(edge_code)
        return self

    def code_markdown(self):
        #self.code_create()
        self.code()
        rendered_lines = self.mermaid_code
        markdown = ['#### Mermaid Graph',
                    "```mermaid"        ,
                    *rendered_lines     ,
                    "```"               ]

        return '\n'.join(markdown)



    def graph_header(self):
        value = self.render_config.diagram_type.name
        return f'{value} {self.render_config.diagram_direction.name}'

    def render_edge(self,edge):
        from_node     = self.graph.node(edge.from_node_id)
        to_node       = self.graph.node(edge.to_node_id  )
        from_node_key = safe_str(from_node.key)
        to_node_key   = safe_str(to_node  .key)
        if edge.edge_config.output_node_from:
            from_node_key =  self.render_node(from_node, include_padding=False)
        if edge.edge_config.output_node_to:
            to_node_key   = self.render_node(to_node, include_padding=False   )
        if edge.edge_config.edge_mode == 'lr_using_pipe':
            link_code      = f'-->|{edge.label}|'
        elif edge.label:
            link_code      = f'--"{edge.label}"-->'
        else:
            link_code      = '-->'
        edge_code      = f'{LINE_PADDING}{from_node_key} {link_code} {to_node_key}'
        return edge_code

    def print_code(self):
        print(self.code())

    def render_node(self, node: Domain__Mermaid__Node, include_padding=True):
        node_data = node.node_data
        node_label  = node.label
        node_key    = node.key
        left_char, right_char = node_data.node_shape.value

        if node_data.markdown:
            label = f'`{node_label}`'
        else:
            label = node_label

        if node_data.show_label is False:
            node_code = f'{node_key}'
        else:
            if node_data.wrap_with_quotes is False:
                node_code = f'{node_key}{left_char}{label}{right_char}'
            else:
                node_code = f'{node_key}{left_char}"{label}"{right_char}'

        if include_padding:
            node_code = f'{LINE_PADDING}{node_code}'
        return node_code

    def reset_code(self):
        self.mermaid_code = []
        return self

    def save(self, target_file=None):
        file_path = target_file or '/tmp/mermaid.md'

        with open(file_path, 'w') as file:
            file.write(self.code_markdown())
        return file_path