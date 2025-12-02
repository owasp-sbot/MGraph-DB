from mgraph_db.mgraph.schemas.safe_str.Safe_Str__Graph__Path import Safe_Str__Graph__Path


class Node_Path(Safe_Str__Graph__Path):
    """Path identifier for a node within a graph.

    Used to classify nodes with a string-based identifier, similar to
    how node_type provides Python type classification. Multiple nodes
    can share the same path (1:many relationship).

    Examples:
        - html.body.div.p
        - config.database.connection
        - user.profile.settings
        - article.section[1].paragraph[2]
    """
    pass