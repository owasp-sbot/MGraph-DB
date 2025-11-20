from typing                          import Dict, Type
from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__MGraph__Diff__Values(Type_Safe):                                # Represents differences between value nodes
    added_values         : Dict[Type, set[str]]             # Values added by type
    removed_values       : Dict[Type, set[str]]             # Values removed by type
