from mgraph_db.mgraph.schemas.safe_str.Safe_Str__Graph__Path import Safe_Str__Graph__Path

class Graph_Path(Safe_Str__Graph__Path):
    """Path identifier for a graph.

    Used to provide a string-based identifier for an entire graph,
    enabling REST API access without Python type resolution.

    Examples:
        - service.users.graph
        - app.config.settings
        - document.html.parsed
    """
    pass