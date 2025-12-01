from mgraph_db.mgraph.schemas.safe_str.Safe_Str__Graph__Path import Safe_Str__Graph__Path


class Edge_Path(Safe_Str__Graph__Path):
    """Path identifier for an edge within a graph.

    Used to classify edges with a string-based identifier, similar to
    how edge_type provides Python type classification. Multiple edges
    can share the same path (1:many relationship).

    Examples:
        - relationship.contains
        - document.parent_child
        - config.references
        - html.element.child[1]
    """
    pass