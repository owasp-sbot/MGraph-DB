from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__MGraph__Index__Config(Type_Safe):
    edges_enabled  : bool = True      # Edge-node relationship tracking
    types_enabled  : bool = True      # Node/edge type indexing
    labels_enabled : bool = True      # Predicate/label indexing
    paths_enabled  : bool = True      # Node/edge path indexing
    values_enabled : bool = True      # Value hash indexing