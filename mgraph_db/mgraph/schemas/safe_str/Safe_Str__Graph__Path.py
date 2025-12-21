import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

SAFE_STR__GRAPH__PATH__REGEX      = re.compile(r'[^a-zA-Z0-9_/\-.:\[\]]')
SAFE_STR__GRAPH__PATH__MAX_LENGTH = 512

class Safe_Str__Graph__Path(Safe_Str):
    """Safe string for graph element paths.

    Provides a REST-friendly string-based identifier for graph elements
    that coexists with Python type fields. Paths enable structural/positional
    identification without requiring Python type resolution.

    Allowed characters:
        - a-zA-Z0-9 : Base identifiers
        - _         : Word separation (Python style)
        - -         : Word separation (kebab style)
        - .         : Hierarchy separator
        - :         : Namespace separator
        - /         : Path separator
        - []        : Index notation

    Examples:
        - html.body.div.p[1]
        - node.path:html.body.section
        - config.database.timeout
        - Domain__Node__Person (Python type names are valid)

    Max length: 512 characters - accommodates deep hierarchies while
    preventing unbounded strings.
    """
    regex           = SAFE_STR__GRAPH__PATH__REGEX
    max_length      = SAFE_STR__GRAPH__PATH__MAX_LENGTH
    allow_empty     = True
    trim_whitespace = True