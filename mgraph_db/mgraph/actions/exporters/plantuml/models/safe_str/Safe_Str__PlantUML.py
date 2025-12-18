import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                   import Safe_Str


class Safe_Str__PlantUML(Safe_Str):                                                   # Safe string for PlantUML DSL code
    regex           = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')                      # only remove control chars (not @, newlines, etc)
    max_length      = 1024 * 1024                                                     # 1MB max (diagrams can be large)
    trim_whitespace = False                                                           # preserve whitespace in DSL

    # PlantUML DSL requires:
    # - @ for directives (@startuml, @enduml)
    # - \n for line breaks
    # - # for colors (#LightBlue)
    # - " for labels ("text")
    # - <> for stereotypes (<<type>>)
    # - --> ..> -> for arrows
    # - : for labels on edges
    # - {} for notes/groups
    # - [] for formatting
    # - | for separators
    # - * + - for lists/bullets