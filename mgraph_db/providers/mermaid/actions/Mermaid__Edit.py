from osbot_utils.type_safe.type_safe_core.decorators.type_safe              import type_safe
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Node               import Domain__Mermaid__Node
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Render__Config    import Schema__Mermaid__Render__Config
from osbot_utils.utils.Misc                                                 import random_text
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Edge               import Domain__Mermaid__Edge
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Diagram_Direction import Schema__Mermaid__Diagram__Direction
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id           import Safe_Id
from mgraph_db.providers.mermaid.actions.Mermaid__Data                      import Mermaid__Data
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Diagram__Type     import Schema__Mermaid__Diagram__Type
from osbot_utils.decorators.methods.cache_on_self                           import cache_on_self
from mgraph_db.mgraph.actions.MGraph__Edit                                  import MGraph__Edit
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Graph              import Domain__Mermaid__Graph


class Mermaid__Edit(MGraph__Edit):
    graph      : Domain__Mermaid__Graph

    def add_directive(self, directive):
        self.render_config().directives.append(directive)
        return self

    @type_safe
    def add_edge(self, from_node_key:Safe_Id, to_node_key:Safe_Id, label:str=None) -> Domain__Mermaid__Edge:
        nodes__by_key = self.data().nodes__by_key()
        from_node     = nodes__by_key.get(from_node_key)            # todo: add method to data to get these nodes
        to_node       = nodes__by_key.get(to_node_key  )            # todo: add config option to auto create node on edges (where that node doesn't exist)
        if from_node is None:
            from_node = self.new_node(key=from_node_key)
        if to_node  is None:
            to_node = self.new_node(key=to_node_key)

        from_node_id    = from_node.node_id
        to_node_id      = to_node.node_id
        edge = self.graph.new_edge(from_node_id=from_node_id, to_node_id=to_node_id)
        if label:
            edge.edge.data.label = label                                             # todo: find a better way to set these properties (this
        return edge

    def add_node(self, **kwargs) -> Domain__Mermaid__Node:                          # todo: see if we need this method
        if 'key' in kwargs and type(kwargs['key']) is str:
            kwargs['key'] = Safe_Id(kwargs['key'])                                  # todo: figure out best way todo this, but the test test_example_* use this a lot (with pure str)
        return self.new_node(**kwargs)

    @cache_on_self
    def data(self):
        return Mermaid__Data(graph=self.graph)                  # todo: look at the best way to do this (i.e. give access to this class the info inside data)

    def new_edge(self) -> Domain__Mermaid__Edge:
        from_node_key = Safe_Id(random_text('node', lowercase=True))
        to_node_key   = Safe_Id(random_text('node', lowercase=True))
        return self.add_edge(from_node_key, to_node_key)

    def render_config(self) -> Schema__Mermaid__Render__Config:         # todo: review this since we really should be able to access the Mermaid__Render__Config outside the Mermaid__Render object
        return self.graph.model.data.render_config

    def set_diagram_type(self, diagram_type):                           # todo: should this be moved into the render class?
        if isinstance(diagram_type, Schema__Mermaid__Diagram__Type):
            self.render_config().diagram_type = diagram_type

    def set_direction(self, direction):
        if isinstance(direction, Schema__Mermaid__Diagram__Direction):
            self.render_config().diagram_direction = direction
        elif isinstance(direction, str) and direction in Schema__Mermaid__Diagram__Direction.__members__:
            self.render_config().diagram_direction = Schema__Mermaid__Diagram__Direction[direction]
        return self                             # If the value can't be set (not a valid name), do nothing

    def new_node(self, **kwargs) -> Domain__Mermaid__Node:
        return super().new_node(**kwargs)