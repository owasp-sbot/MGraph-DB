from typing                                                                           import Dict, Literal
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id       import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label    import Safe_Str__Label

# todo: these should be refactored to Schema__PlantUml__* and placed in a schemas folder


class PlantUML__Config__Display(Type_Safe):                                           # controls what gets shown in output
    show_node_id         : bool                               = False                 # display node IDs in labels
    show_node_type       : bool                               = True                  # display node type names
    #show_node_path       : bool                               = True                 # todo: add support for showing the node path
    show_node_value      : bool                               = True                  # display values for value nodes
    show_edge_predicate  : bool                               = True                  # display edge predicates
    show_edge_type       : bool                               = False                 # display edge type names
    wrap_at              : int                                = 40                    # wrap text at this width


class PlantUML__Config__Node(Type_Safe):                                              # node rendering configuration
    shape                : Literal['rectangle', 'card',                               # PlantUML shape for nodes
                                   'component', 'node',
                                   'actor', 'cloud',
                                   'database', 'folder']      = 'card'
    default_color        : Safe_Str__Id                       = None                  # default background color
    type_colors          : Dict[str, Safe_Str__Id]                                    # type name -> color mapping


class PlantUML__Config__Edge(Type_Safe):                                              # edge rendering configuration
    style                : Literal['-->', '..>', '->', '--|>',                        # arrow style
                                   'o--', '*--']              = '-->'
    default_color        : Safe_Str__Id                       = None                  # default edge color
    predicate_colors     : Dict[str, Safe_Str__Id]                                    # predicate -> color mapping


class PlantUML__Config__Graph(Type_Safe):                                             # graph-level configuration
    direction            : Literal['TB', 'LR', 'BT', 'RL']    = 'TB'                  # layout direction
    title                : Safe_Str__Label                    = None                  # diagram title
    background_color     : Safe_Str__Id                       = None                  # background color
    shadowing            : bool                               = False                 # enable shadows


class PlantUML__Config(Type_Safe):                                                    # main configuration container
    graph                : PlantUML__Config__Graph                                    # graph-level settings
    node                 : PlantUML__Config__Node                                     # node settings
    edge                 : PlantUML__Config__Edge                                     # edge settings
    display              : PlantUML__Config__Display                                  # display settings
