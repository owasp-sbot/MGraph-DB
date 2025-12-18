from typing                                                                           import Optional
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label    import Safe_Str__Label
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                                     import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                     import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Data                              import Schema__MGraph__Edge__Data
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Base                import PlantUML__Base


class PlantUML__Edge__Renderer(PlantUML__Base):                                       # renders a single edge to PlantUML statement
    config               : PlantUML__Config                   = None                  # rendering configuration

    def render(self, edge      : Domain__MGraph__Edge      ,                          # render edge to complete statement
                     from_node : Domain__MGraph__Node      ,
                     to_node   : Domain__MGraph__Node      ,
                     edge_data : Schema__MGraph__Edge__Data) -> str:
        from_id    = self.safe_id(from_node.node_id)                                # sanitized source ID
        to_id      = self.safe_id(to_node.node_id)                                  # sanitized target ID
        arrow      = self.config.edge.style                                           # arrow style from config
        label      = self.build_label(edge, edge_data)                                # build edge label

        if label:                                                                     # statement with label
            return f'{from_id} {arrow} {to_id} : {label}'
        return f'{from_id} {arrow} {to_id}'                                           # statement without label

    def build_label(self, edge      : Domain__MGraph__Edge      ,                     # build edge display label
                          edge_data : Schema__MGraph__Edge__Data) -> Optional[str]:
        parts      = []                                                               # label parts
        display    = self.config.display                                              # display settings

        if display.show_edge_predicate:                                               # add predicate
            predicate = self.extract_predicate(edge)
            if predicate:
                parts.append(str(predicate))

        if display.show_edge_type:                                                    # add edge type
            type_name = self.type_name__from__type(edge.edge_type)
            parts.append(f'<<{type_name}>>')

        return ' '.join(parts) if parts else None

    def extract_predicate(self, edge: Domain__MGraph__Edge) -> Optional[Safe_Str__Label]:  # extract predicate from edge
        try:
            edge_label = edge.edge_label()
            if edge_label and hasattr(edge_label, 'predicate'):
                predicate = edge_label.predicate
                if predicate:
                    return Safe_Str__Label(str(predicate))
        except Exception:
            pass
        return None
