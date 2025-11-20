from mgraph_db.mgraph.domain.Domain__MGraph__Edge                      import Domain__MGraph__Edge
from mgraph_db.providers.mermaid.models.Model__Mermaid__Edge           import Model__Mermaid__Edge
from mgraph_db.providers.mermaid.models.Model__Mermaid__Graph          import Model__Mermaid__Graph
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge__Config import Schema__Mermaid__Edge__Config
from osbot_utils.type_safe.type_safe_core.methods.type_safe_property   import set_as_property


class Domain__Mermaid__Edge(Domain__MGraph__Edge):
    edge  : Model__Mermaid__Edge
    graph : Model__Mermaid__Graph

    edge_config  = set_as_property('edge.data', 'edge_config', Schema__Mermaid__Edge__Config)
    from_node_id = set_as_property('edge.data', 'from_node_id')
    label        = set_as_property('edge.data', 'label'       )
    to_node_id   = set_as_property('edge.data', 'to_node_id'  )


    # def config(self) -> Schema__Mermaid__Edge__Config:
    #     return super().config()

    def edge_mode(self, edge_mode):
        self.edge_config.edge_mode = edge_mode
        return self

    def edge_mode__lr_using_pipe(self):
        return self.edge_mode('lr_using_pipe')

    def output_node_from(self, value=True):
        self.edge_config.output_node_from = value
        return self

    def output_node_to(self, value=True):
        self.edge_config.output_node_to = value
        return self