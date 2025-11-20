from typing                                                                                 import Dict, Any, Optional, Callable
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Layout__Engine      import MGraph__Export__Dot__Layout__Engine
from osbot_utils.utils.Lists                                                                import unique
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Base                                import MGraph__Export__Base
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config              import MGraph__Export__Dot__Config
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Font        import MGraph__Export__Dot__Config__Font
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Shape       import MGraph__Export__Dot__Config__Shape
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Type__Node  import MGraph__Export__Dot__Config__Type__Node
from mgraph_db.mgraph.actions.exporters.dot.render.MGraph__Export__Dot__Edge__Renderer      import MGraph__Export__Dot__Edge__Renderer
from mgraph_db.mgraph.actions.exporters.dot.render.MGraph__Export__Dot__Format__Generator   import MGraph__Export__Dot__Format__Generator
from mgraph_db.mgraph.actions.exporters.dot.render.MGraph__Export__Dot__Node__Renderer      import MGraph__Export__Dot__Node__Renderer
from mgraph_db.mgraph.actions.exporters.dot.render.MGraph__Export__Dot__Style__Manager      import MGraph__Export__Dot__Style__Manager
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                                           import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                           import Domain__MGraph__Node

class MGraph__Export__Dot(MGraph__Export__Base):
    config          : MGraph__Export__Dot__Config                                                    # Configuration for DOT export
    on_add_node     : Callable[[Domain__MGraph__Node, Dict[str, Any]], Dict[str, Any]]             # Optional node callback
    on_add_edge     : Callable[[Domain__MGraph__Edge, Domain__MGraph__Node, Domain__MGraph__Node, Dict[str, Any]], None]  # Optional edge callback
    node_renderer   : MGraph__Export__Dot__Node__Renderer       = None
    edge_renderer   : MGraph__Export__Dot__Edge__Renderer       = None
    style_manager   : MGraph__Export__Dot__Style__Manager       = None
    format_generator: MGraph__Export__Dot__Format__Generator    = None
    dot_code        : str                                        = None


    def __init__(self, graph, config: Optional[MGraph__Export__Dot__Config] = None):
        super().__init__(graph=graph)
        self.config           = config or MGraph__Export__Dot__Config()           #todo: refactor this to a setup method (since ctor's should really not be doing much                                                               # Initialize component classes
        self.node_renderer    = MGraph__Export__Dot__Node__Renderer   (config=self.config, graph=self.graph)
        self.edge_renderer    = MGraph__Export__Dot__Edge__Renderer   (config=self.config, graph=self.graph)
        self.style_manager    = MGraph__Export__Dot__Style__Manager   (config=self.config, graph=self.graph)
        self.format_generator = MGraph__Export__Dot__Format__Generator(config=self.config, graph=self.graph)

    def create_node_data(self, node) -> Dict[str, Any]:                                        # Create node data for DOT export
        attrs = self.node_renderer.create_node_attributes(node)
        attrs = unique(attrs)                           # todo: fix bug in create_node_attributes where multiple style statements can be created
        node_data = {'id'   : str(node.node_id),
                     'attrs': attrs }

        if self.on_add_node:
            self.on_add_node(node, node_data)
        return node_data

    def create_edge_data(self, edge) -> Dict[str, Any]:                                        # Create edge data for DOT export
        attrs = self.edge_renderer.create_edge_attributes(edge)
        edge_data = {'id'    : str(edge.edge_id),
                     'source': str(edge.from_node_id()),
                     'target': str(edge.to_node_id()),
                     'type'  : edge.edge.data.edge_type.__name__,
                     'attrs' : attrs}

        if self.on_add_edge:
            from_node = edge.from_node()
            to_node = edge.to_node()
            if from_node and to_node:
                self.on_add_edge(edge, from_node, to_node, edge_data)
        return edge_data

    def format_output(self) -> str:                                                            # Format complete DOT output
        lines = self.format_generator.generate_graph_header()

        for node_data in self.context.nodes.values():
            lines.append(self.node_renderer.format_node_definition(
                node_data["id"], node_data["attrs"]))

        for edge_data in self.context.edges.values():
            lines.append(self.edge_renderer.format_edge_definition(
                edge_data["source"], edge_data["target"], edge_data["attrs"]))

        lines.append('}')
        self.dot_code =  '\n'.join(lines)
        if self.config.render.print_dot_code:
            print()
            print(self.dot_code)
        return self.dot_code


    # Configuration setter methods

    def ensure_type_shape(self, node_type: type):                                                   # Helper methods
        if node_type not in self.config.type.shapes:
            self.config.type.shapes[node_type] = MGraph__Export__Dot__Config__Shape()
        return self.config.type.shapes[node_type]

    def ensure_type_font(self, node_type: type):
        if node_type not in self.config.type.fonts:
            self.config.type.fonts[node_type] = MGraph__Export__Dot__Config__Font()
        return self.config.type.fonts[node_type]

    def ensure_edge_node_config(self, edge_type: type, config_dict: Dict[type, MGraph__Export__Dot__Config__Type__Node]) -> MGraph__Export__Dot__Config__Type__Node:
        if edge_type not in config_dict:
            config_dict[edge_type] = MGraph__Export__Dot__Config__Type__Node()
            config_dict[edge_type].fonts  = MGraph__Export__Dot__Config__Font()
            config_dict[edge_type].shapes = MGraph__Export__Dot__Config__Shape()
        return config_dict[edge_type]

    def ensure_value_type_shape(self, value_type: type):
        if value_type not in self.config.type.value_shapes:
            self.config.type.value_shapes[value_type] = MGraph__Export__Dot__Config__Shape()
        return self.config.type.value_shapes[value_type]

    def ensure_value_type_font(self, value_type: type):
        if value_type not in self.config.type.value_fonts:
            self.config.type.value_fonts[value_type] = MGraph__Export__Dot__Config__Font()
        return self.config.type.value_fonts[value_type]

    def print_dot_code                 (self): return self.set_render__print_dot_code()

    def set_render__print_dot_code     (self): self.config.render.print_dot_code      = True ; return self
    def set_render__label_show_var_name(self): self.config.render.label_show_var_name = True ; return self

    def set_edge__color          (self, color    : str  ): self.config.edge.color      = color       ; return self
    def set_edge__font__size     (self, size     : int  ): self.config.edge.font.size  = size        ; return self
    def set_edge__font__color    (self, color    : str  ): self.config.edge.font.color = color       ; return self
    def set_edge__font__name     (self, name     : str  ): self.config.edge.font.name  = name        ; return self
    def set_edge__style          (self, style    : str  ): self.config.edge.style      = style       ; return self
    def set_edge__arrow_size     (self, size     : float): self.config.edge.arrow_size = size        ; return self

    def set_edge__arrow_head         (self, head  : str  ): self.config.edge.arrow_head = head       ; return self
    def set_edge__arrow_head__dot    (self               ): self.config.edge.arrow_head = 'dot'      ; return self
    def set_edge__arrow_head__vee    (self               ): self.config.edge.arrow_head = 'vee'      ; return self
    def set_edge__arrow_head__tee    (self               ): self.config.edge.arrow_head = 'tee'      ; return self
    def set_edge__arrow_head__none   (self               ): self.config.edge.arrow_head = 'none'     ; return self
    def set_edge__arrow_head__normal (self               ): self.config.edge.arrow_head = 'normal'     ; return self
    def set_edge__arrow_head__diamond(self               ): self.config.edge.arrow_head = 'diamond'  ; return self
    def set_edge__arrow_head__crow   (self               ): self.config.edge.arrow_head = 'crow'     ; return self


    def set_node__fill_color     (self, color    : str  ): self.config.node.shape.fill_color = color    ; return self
    def set_node__font__color    (self, color    : str  ): self.config.node.font.color       = color    ; return self
    def set_node__font__name     (self, name     : str  ): self.config.node.font.name        = name     ; return self
    def set_node__font__size     (self, size     : int  ): self.config.node.font.size        = size     ; return self
    def set_node__shape__rounded (self                  ): self.config.node.shape.rounded    = True     ; return self
    def set_node__shape__width   (self, width    : float): self.config.node.shape.width      = width    ; return self
    def set_node__shape__height  (self, height   : float): self.config.node.shape.height     = height   ; return self
    def set_node__shape__fixed   (self                  ): self.config.node.shape.fixed_size = True     ; return self

    def set_node__shape__type                (self, shape    : str  ): self.config.node.shape.type = shape          ; return self
    def set_node__shape__type__box           (self,                 ): self.config.node.shape.type = 'box'          ; return self
    def set_node__shape__type__circle        (self,                 ): self.config.node.shape.type = 'circle'       ; return self
    def set_node__shape__type__ellipse       (self,                 ): self.config.node.shape.type = 'ellipse'      ; return self
    def set_node__shape__type__point         (self,                 ): self.config.node.shape.type = 'point'        ; return self
    def set_node__shape__type__diamond       (self,                 ): self.config.node.shape.type = 'diamond'      ; return self
    def set_node__shape__type__plaintext     (self,                 ): self.config.node.shape.type = 'plaintext'    ; return self
    def set_node__shape__type__polygon       (self,                 ): self.config.node.shape.type = 'polygon'      ; return self
    def set_node__shape__type__star          (self,                 ): self.config.node.shape.type = 'star'         ; return self
    def set_node__shape__type__triangle      (self,                 ): self.config.node.shape.type = 'triangle'     ; return self
    def set_node__shape__type__trapezium     (self,                 ): self.config.node.shape.type = 'trapezium'    ; return self
    def set_node__shape__type__parallelogram (self,                 ): self.config.node.shape.type = 'parallelogram'; return self
    def set_node__shape__type__house         (self,                 ): self.config.node.shape.type = 'house'        ; return self
    def set_node__shape__type__hexagon       (self,                 ): self.config.node.shape.type = 'hexagon'      ; return self
    def set_node__shape__type__octagon       (self,                 ): self.config.node.shape.type = 'octagon'      ; return self



    def set_node__style           (self, style    : str  ): self.config.node.shape.style      = style    ; return self

    def set_graph__layout_engine  (self, engine   : str  ): self.config.graph.layout_engine   = engine   ; return self
    def set_graph__margin         (self, value    : float): self.config.graph.margin          = value    ; return self
    def set_graph__node_sep       (self, value    : float): self.config.graph.node_sep        = value    ; return self
    def set_graph__rank_sep       (self, value    : float): self.config.graph.rank_sep        = value    ; return self
    def set_graph__rank_dir       (self, direction: str  ): self.config.graph.rank_dir        = direction; return self
    def set_graph__splines        (self, value    : float): self.config.graph.splines         = value    ; return self
    def set_graph__epsilon        (self, value    : float): self.config.graph.epsilon         = value    ; return self
    def set_graph__spring_constant(self, value    : float): self.config.graph.spring_constant = value    ; return self

    def set_graph__title             (self, value    : str  ): self.config.graph.title             = value    ; return self
    def set_graph__title__font__size (self, value    : float): self.config.graph.title__font.size  = value    ; return self
    def set_graph__title__font__color(self, value    : str  ): self.config.graph.title__font.color = value    ; return self
    def set_graph__title__font__name (self, value    : str  ): self.config.graph.title__font.name  = value    ; return self
    def set_graph__background__color (self, value    : str  ): self.config.graph.background_color  = value    ; return self

    def set_graph__overlap           (self, value   : str  ): self.config.graph.overlap   = value     ; return self
    def set_graph__overlap__false    (self,                ): self.config.graph.overlap   = 'false'   ; return self
    def set_graph__overlap__scale    (self,                ): self.config.graph.overlap   = 'scale'   ; return self
    def set_graph__overlap__prism    (self,                ): self.config.graph.overlap   = 'prism'   ; return self
    def set_graph__overlap__prism1000 (self,               ): self.config.graph.overlap   = 'prism1000' ; return self
    def set_graph__overlap__vpsc      (self,               ): self.config.graph.overlap   = 'vpsc'      ; return self
    def set_graph__overlap__ortho     (self,               ): self.config.graph.overlap   = 'ortho'     ; return self
    def set_graph__overlap__orthoxy   (self,               ): self.config.graph.overlap   = 'orthoxy'   ; return self
    def set_graph__overlap__orthoyx   (self,               ): self.config.graph.overlap   = 'orthoyx'   ; return self
    def set_graph__overlap__ipsep     (self,               ): self.config.graph.overlap   = 'ipsep'     ; return self
    def set_graph__overlap__compress  (self,               ): self.config.graph.overlap   = 'compress'  ; return self
    def set_graph__overlap__true      (self,               ): self.config.graph.overlap   = 'true'      ; return self  # Default behavior

    def set_graph__layout_engine__dot   (self): return self.set_graph__layout_engine(MGraph__Export__Dot__Layout__Engine.DOT   .value)
    def set_graph__layout_engine__neato (self): return self.set_graph__layout_engine(MGraph__Export__Dot__Layout__Engine.NEATO .value)
    def set_graph__layout_engine__twopi (self): return self.set_graph__layout_engine(MGraph__Export__Dot__Layout__Engine.TWOPI .value)
    def set_graph__layout_engine__circo (self): return self.set_graph__layout_engine(MGraph__Export__Dot__Layout__Engine.CIRCO .value)
    def set_graph__layout_engine__fdp   (self): return self.set_graph__layout_engine(MGraph__Export__Dot__Layout__Engine.FDP   .value)
    def set_graph__layout_engine__sfdp  (self): return self.set_graph__layout_engine(MGraph__Export__Dot__Layout__Engine.SFDP  .value)
    def set_graph__layout_engine__osage (self): return self.set_graph__layout_engine(MGraph__Export__Dot__Layout__Engine.OSAGE .value)

    def set_graph__splines__line        (self): return self.set_graph__splines ('line'    )
    def set_graph__splines__polyline    (self): return self.set_graph__splines ('polyline')
    def set_graph__splines__ortho       (self): return self.set_graph__splines ('ortho'   )
    def set_graph__splines__curved      (self): return self.set_graph__splines ('curved'  )
    def set_graph__rank_dir__tb         (self): return self.set_graph__rank_dir('TB'      )
    def set_graph__rank_dir__lr         (self): return self.set_graph__rank_dir('LR'      )
    def set_graph__rank_dir__bt         (self): return self.set_graph__rank_dir('BT'      )
    def set_graph__rank_dir__rl         (self): return self.set_graph__rank_dir('RL'      )

    def show_edge__id                (self): self.config.display.edge_id             = True      ; return self
    def show_edge__predicate         (self): self.config.display.edge_predicate      = True      ; return self
    def show_edge__predicate__str    (self): self.config.display.edge_predicate_str  = True      ; return self
    def show_edge__type              (self): self.config.display.edge_type           = True      ; return self
    def show_edge__type_full_name    (self): self.config.display.edge_type_full_name = True      ; return self
    def show_edge__type__str         (self): self.config.display.edge_type_str       = True      ; return self


    def show_node__id                (self): self.config.display.node_id             = True      ; return self
    def show_node__value             (self): self.config.display.node_value          = True      ; return self

    def show_node__value__key        (self): self.config.display.node_value_key      = True      ; return self
    def show_node__value__type       (self): self.config.display.node_value_type     = True      ; return self
    def show_node__type              (self): self.config.display.node_type           = True      ; return self
    def show_node__type_full_name    (self): self.config.display.node_type_full_name = True      ; return self

    def set_node__type_fill_color(self, node_type: type, color: str): self.ensure_type_shape(node_type).fill_color = color; return self
    def set_node__type_font_color(self, node_type: type, color: str): self.ensure_type_font (node_type).color      = color; return self
    def set_node__type_font_size (self, node_type: type, size : int): self.ensure_type_font (node_type).size       = size ; return self
    def set_node__type_font_name (self, node_type: type, name : str): self.ensure_type_font (node_type).name       = name ; return self
    def set_node__type_rounded   (self, node_type: type             ):self.ensure_type_shape(node_type).rounded    = True ; return self
    def set_node__type_shape     (self, node_type: type, shape: str): self.ensure_type_shape(node_type).type       = shape; return self
    def set_node__type_style     (self, node_type: type, style: str): self.ensure_type_shape(node_type).style      = style; return self


    def set_edge__type_color(self, edge_type: type, color: str):
        if not self.config.type.edge_color: self.config.type.edge_color = {}
        self.config.type.edge_color[edge_type] = color
        return self

    def set_edge__type_style(self, edge_type: type, style: str):
        if not self.config.type.edge_style: self.config.type.edge_style = {}
        self.config.type.edge_style[edge_type] = style
        return self


    # Methods for source nodes (edge starts from)
    def set_edge_from_node__type_fill_color (self, edge_type: type, color: str): self.ensure_edge_node_config(edge_type, self.config.type.edge_from).shapes.fill_color = color; return self
    def set_edge_from_node__type_font_color (self, edge_type: type, color: str): self.ensure_edge_node_config(edge_type, self.config.type.edge_from).fonts.color       = color; return self
    def set_edge_from_node__type_font_size  (self, edge_type: type, size : int): self.ensure_edge_node_config(edge_type, self.config.type.edge_from).fonts.size        = size ; return self
    def set_edge_from_node__type_font_name  (self, edge_type: type, name : str): self.ensure_edge_node_config(edge_type, self.config.type.edge_from).fonts.name        = name ; return self
    def set_edge_from_node__type_shape      (self, edge_type: type, shape: str): self.ensure_edge_node_config(edge_type, self.config.type.edge_from).shapes.type       = shape; return self
    def set_edge_from_node__type_style      (self, edge_type: type, style: str): self.ensure_edge_node_config(edge_type, self.config.type.edge_from).shapes.style      = style; return self

    # Methods for target nodes (edge points to)
    def set_edge_to_node__type_fill_color   (self, edge_type: type, color: str): self.ensure_edge_node_config(edge_type, self.config.type.edge_to).shapes.fill_color = color; return self
    def set_edge_to_node__type_font_color   (self, edge_type: type, color: str): self.ensure_edge_node_config(edge_type, self.config.type.edge_to).fonts.color       = color; return self
    def set_edge_to_node__type_font_size    (self, edge_type: type, size : int): self.ensure_edge_node_config(edge_type, self.config.type.edge_to).fonts.size        = size ; return self
    def set_edge_to_node__type_font_name    (self, edge_type: type, name : str): self.ensure_edge_node_config(edge_type, self.config.type.edge_to).fonts.name        = name ; return self
    def set_edge_to_node__type_shape        (self, edge_type: type, shape: str): self.ensure_edge_node_config(edge_type, self.config.type.edge_to).shapes.type       = shape; return self
    def set_edge_to_node__type_style        (self, edge_type: type, style: str): self.ensure_edge_node_config(edge_type, self.config.type.edge_to).shapes.style      = style; return self

    # methods for value_type styling
    def set_value_type_shape                (self, value_type: type, shape: str): self.ensure_value_type_shape(value_type).type       = shape; return self
    def set_value_type_fill_color           (self, value_type: type, color: str): self.ensure_value_type_shape(value_type).fill_color = color; return self
    def set_value_type_style                (self, value_type: type, style: str): self.ensure_value_type_shape(value_type).style      = style; return self
    def set_value_type_rounded              (self, value_type: type            ): self.ensure_value_type_shape(value_type).rounded    = True ; return self

    def set_value_type_font_name            (self, value_type: type, name  : str  ): self.ensure_value_type_font(value_type).name        = name ; return self
    def set_value_type_font_size            (self, value_type: type, size  : int  ): self.ensure_value_type_font(value_type).size        = size ; return self
    def set_value_type_font_color           (self, value_type: type, color : str  ): self.ensure_value_type_font(value_type).color       = color; return self
    def set_value_type_width                (self, value_type: type, width : float): self.ensure_value_type_shape(value_type).width      = width ; return self
    def set_value_type_height               (self, value_type: type, height: float): self.ensure_value_type_shape(value_type).height     = height; return self
    def set_value_type_size                 (self, value_type: type, value : float): self.ensure_value_type_shape(value_type).height     = value; self.ensure_value_type_shape(value_type).width = value; return self
    def set_value_type_fixed                (self, value_type: type               ) : self.ensure_value_type_shape(value_type).fixed_size  = True  ; return self
