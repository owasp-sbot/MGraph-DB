from typing                                                                           import Optional, Callable
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Context             import PlantUML__Context
from mgraph_db.mgraph.actions.exporters.plantuml.models.safe_str.Safe_Str__PlantUML   import Safe_Str__PlantUML
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                                    import Domain__MGraph__Graph
from mgraph_db.mgraph.index.MGraph__Index                                             import MGraph__Index
from mgraph_db.mgraph.actions.MGraph__Data                                            import MGraph__Data
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Graph
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Node
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Edge
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Display
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Node__Renderer      import PlantUML__Node__Renderer
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Edge__Renderer      import PlantUML__Edge__Renderer
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Format__Generator   import PlantUML__Format__Generator




class MGraph__Export__PlantUML(Type_Safe):                                            # main PlantUML exporter orchestrator
    graph                : Domain__MGraph__Graph              = None                  # graph to export
    index                : MGraph__Index                      = None                  # graph index
    data                 : MGraph__Data                       = None                  # graph data accessor
    config               : PlantUML__Config                   = None                  # rendering configuration
    context              : PlantUML__Context                  = None                  # rendering context

    node_renderer        : PlantUML__Node__Renderer           = None                  # node renderer instance
    edge_renderer        : PlantUML__Edge__Renderer           = None                  # edge renderer instance
    format_generator     : PlantUML__Format__Generator        = None                  # format generator instance

    on_add_node          : Optional[Callable]                 = None                  # callback: on_add_node(node, node_data) -> Optional[str]
    on_add_edge          : Optional[Callable]                 = None                  # callback: on_add_edge(edge, from_node, to_node, edge_data) -> Optional[str]

    def setup(self):                                                                  # initialize renderers and config
        if not self.config:                                                           # create default config
            self.config = PlantUML__Config(
                graph   = PlantUML__Config__Graph  ()                              ,
                node    = PlantUML__Config__Node   ()                              ,
                edge    = PlantUML__Config__Edge   ()                              ,
                display = PlantUML__Config__Display()                              )

        if not self.context:                                                          # create context
            self.context = PlantUML__Context()

        if not self.node_renderer:                                                    # create node renderer
            self.node_renderer = PlantUML__Node__Renderer(
                graph  = self.graph                                                ,
                index  = self.index                                                ,
                config = self.config                                               )

        if not self.edge_renderer:                                                    # create edge renderer
            self.edge_renderer = PlantUML__Edge__Renderer(
                graph  = self.graph                                                ,
                index  = self.index                                                ,
                config = self.config                                               )

        if not self.format_generator:                                                 # create format generator
            self.format_generator = PlantUML__Format__Generator(
                config = self.config                                               )

        return self

    def render(self) -> Safe_Str__PlantUML:                                             # render graph to PlantUML DSL
        self.setup()                                                                  # ensure initialization
        self.context.nodes = []                                                       # reset context
        self.context.edges = []

        lines = []                                                                    # output lines

        lines.append(self.format_generator.start_uml())                               # @startuml
        lines.extend(self.format_generator.skin_params())                             # skinparam directives
        lines.extend(self.format_generator.graph_directives())                        # graph directives
        lines.append('')                                                              # blank line

        self.render_nodes()                                                           # render all nodes
        lines.extend(self.context.nodes)
        lines.append('')                                                              # blank line

        self.render_edges()                                                           # render all edges
        lines.extend(self.context.edges)

        lines.append(self.format_generator.end_uml())                                 # @enduml

        return Safe_Str__PlantUML('\n'.join(lines))

    def render_nodes(self):                                                           # render all nodes to context
        if not self.data:
            return

        for node_id in self.data.nodes_ids():
            node = self.data.node(node_id)
            if not node:
                continue

            node_data = None
            try:
                node_data = node.node_data()
            except Exception:
                pass

            if self.on_add_node:                                                      # check callback
                custom = self.on_add_node(node, node_data)
                if custom is not None:
                    self.context.nodes.append(custom)
                    continue

            statement = self.node_renderer.render(node, node_data)                    # default render
            self.context.nodes.append(statement)

    def render_edges(self):                                                           # render all edges to context
        if not self.data:
            return

        for edge_id in self.data.edges_ids():
            edge = self.data.edge(edge_id)
            if not edge:
                continue

            from_node = self.data.node(edge.from_node_id())
            to_node   = self.data.node(edge.to_node_id())
            if not from_node or not to_node:
                continue

            edge_data = None
            try:
                edge_data = edge.edge_data()
            except Exception:
                pass

            if self.on_add_edge:                                                      # check callback
                custom = self.on_add_edge(edge, from_node, to_node, edge_data)
                if custom is not None:
                    self.context.edges.append(custom)
                    continue

            statement = self.edge_renderer.render(edge, from_node, to_node, edge_data)  # default render
            self.context.edges.append(statement)

    def set_direction(self, direction: str) -> 'MGraph__Export__PlantUML':            # fluent: set layout direction
        self.setup()
        self.config.graph.direction = direction
        return self

    def set_title(self, title: str) -> 'MGraph__Export__PlantUML':                    # fluent: set title
        self.setup()
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label import Safe_Str__Label
        self.config.graph.title = Safe_Str__Label(title)
        return self

    def set_node_shape(self, shape: str) -> 'MGraph__Export__PlantUML':               # fluent: set node shape
        self.setup()
        self.config.node.shape = shape
        return self

    def set_show_node_type(self, enabled: bool) -> 'MGraph__Export__PlantUML':        # fluent: show/hide node types
        self.setup()
        self.config.display.show_node_type = enabled
        return self

    def set_show_node_value(self, enabled: bool) -> 'MGraph__Export__PlantUML':       # fluent: show/hide node values
        self.setup()
        self.config.display.show_node_value = enabled
        return self

    def set_show_edge_predicate(self, enabled: bool) -> 'MGraph__Export__PlantUML':   # fluent: show/hide predicates
        self.setup()
        self.config.display.show_edge_predicate = enabled
        return self

    def left_to_right(self) -> 'MGraph__Export__PlantUML':                            # fluent: horizontal layout
        return self.set_direction('LR')

    def top_to_bottom(self) -> 'MGraph__Export__PlantUML':                            # fluent: vertical layout
        return self.set_direction('TB')
