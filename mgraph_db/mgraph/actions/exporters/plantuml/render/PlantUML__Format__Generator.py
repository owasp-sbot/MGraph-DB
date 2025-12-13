from typing                                                                           import List
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe

from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                                        import PlantUML__Config


class PlantUML__Format__Generator(Type_Safe):                                         # generates PlantUML format directives
    config               : PlantUML__Config                   = None                  # rendering configuration

    def start_uml(self) -> str:                                                       # emit @startuml directive
        return '@startuml'

    def end_uml(self) -> str:                                                         # emit @enduml directive
        return '@enduml'

    def graph_directives(self) -> List[str]:                                          # emit graph-level directives
        lines      = []                                                               # accumulate directives
        graph_cfg  = self.config.graph                                                # graph config

        if graph_cfg.direction == 'LR':                                               # horizontal layout
            lines.append('left to right direction')
        elif graph_cfg.direction == 'RL':                                             # reverse horizontal
            lines.append('right to left direction')
        elif graph_cfg.direction == 'BT':                                             # bottom to top
            lines.append('bottom to top direction')
                                                                                      # TB is default, no directive needed

        if graph_cfg.title:                                                           # add title
            lines.append(f'title {graph_cfg.title}')

        return lines

    def skin_params(self) -> List[str]:                                               # emit skinparam directives
        lines      = []                                                               # accumulate directives
        graph_cfg  = self.config.graph                                                # graph config

        lines.append('skinparam backgroundColor transparent')                         # always transparent

        if not graph_cfg.shadowing:                                                   # disable shadows by default
            lines.append('skinparam shadowing false')

        if graph_cfg.background_color:                                                # explicit background
            lines.append(f'skinparam backgroundColor {graph_cfg.background_color}')

        return lines
