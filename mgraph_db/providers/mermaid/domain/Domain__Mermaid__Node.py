from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data   import Schema__Mermaid__Node__Data
from mgraph_db.mgraph.domain.Domain__MGraph__Node                      import Domain__MGraph__Node
from mgraph_db.providers.mermaid.models.Model__Mermaid__Graph          import Model__Mermaid__Graph
from mgraph_db.providers.mermaid.models.Model__Mermaid__Node           import Model__Mermaid__Node
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Shape  import Schema__Mermaid__Node__Shape
from osbot_utils.type_safe.type_safe_core.methods.type_safe_property   import set_as_property

LINE_PADDING = '    '

class Domain__Mermaid__Node(Domain__MGraph__Node):
    node : Model__Mermaid__Node
    graph: Model__Mermaid__Graph

    label     = set_as_property('node.data', 'label'    , str                           )
    key       = set_as_property('node.data', 'key'      , str                           )
    node_data = set_as_property('node.data', 'node_data', Schema__Mermaid__Node__Data)

    def markdown(self, value=True):
        self.node_data.markdown = value
        return self

    # def node_key(self):
    #     return self.node.data.key

    # def node_label(self):
    #     return self.node.data.label

    def shape(self, shape=None):
        self.node_data.node_shape = Schema__Mermaid__Node__Shape.get_shape(shape)
        return self


    def shape_asymmetric        (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.asymmetric        ; return self
    def shape_circle            (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.circle            ; return self
    def shape_cylindrical       (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.cylindrical       ; return self
    def shape_default           (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.default           ; return self
    def shape_double_circle     (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.double_circle     ; return self
    def shape_hexagon           (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.hexagon           ; return self
    def shape_parallelogram     (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.parallelogram     ; return self
    def shape_parallelogram_alt (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.parallelogram_alt ; return self
    def shape_stadium           (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.stadium           ; return self
    def shape_subroutine        (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.subroutine        ; return self
    def shape_rectangle         (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.rectangle         ; return self
    def shape_rhombus           (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.rhombus           ; return self
    def shape_round_edges       (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.round_edges       ; return self
    def shape_trapezoid         (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.trapezoid         ; return self
    def shape_trapezoid_alt     (self): self.node_data.node_shape = Schema__Mermaid__Node__Shape.trapezoid_alt     ; return self



    def wrap_with_quotes(self, value=True):
        self.node_data.wrap_with_quotes = value
        return self

    def show_label(self, value=True):
        self.node_data.show_label = value
        return self