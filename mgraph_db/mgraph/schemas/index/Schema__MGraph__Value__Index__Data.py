from typing                                                         import Dict, Set, Type
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id


class Schema__MGraph__Value__Index__Data(Type_Safe):
    hash_to_node   : Dict[str, Node_Id   ]              # value_hash -> node_id that holds that value
    node_to_hash   : Dict[Node_Id, str   ]              # node_id -> value_hash (for reverse lookup)
    values_by_type : Dict[Type, Set[str]]              # type -> set of value_hashes for that type
    type_by_value  : Dict[str, Type     ]              # value_hash -> type name (for type validation)