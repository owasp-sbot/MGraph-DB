from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from mgraph_db.query.schemas.Schema__MGraph__Query__Export__View    import Schema__MGraph__Query__Export__View
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id  import Graph_Id


class Model__MGraph__Query__Export__View(Type_Safe):
    data: Schema__MGraph__Query__Export__View

    def create_new_graph(self) -> Schema__MGraph__Graph:                                                                # Creates a new empty graph with the same types as source using Type_Safe serialization
        with self.data.source_graph as _:
            type__graph_data   = type(_.graph_data)
            type__schema_types = type(_.schema_types)
            type__schema_graph = type(_)
            graph_data   = type__graph_data.from_json(_.graph_data.json  ())
            schema_types = type__schema_types         .from_json(_.schema_types.json())
            return type__schema_graph(edges        = {}                 ,
                                      graph_data   = graph_data         ,
                                      graph_id     = Graph_Id(Obj_Id()) ,
                                      graph_type   = _.graph_type       ,
                                      nodes        = {}                 ,
                                      schema_types = schema_types       )

    def clone_nodes(self, new_graph: Schema__MGraph__Graph) -> None:                                                    # Clones specified nodes to new graph using Type_Safe serialization
        for node_id in self.data.nodes_ids:
            source_node                  = self.data.source_graph.nodes.get(node_id)
            if source_node:
                new_node                     = source_node.node_type.from_json(source_node.json())
                new_graph.nodes[node_id] = new_node

    def clone_edges(self, new_graph: Schema__MGraph__Graph) -> None:                                                    # Clones specified edges to new graph using Type_Safe serialization
        for edge_id in self.data.edges_ids:
            source_edge                  = self.data.source_graph.edges.get(edge_id)
            if source_edge:
                new_edge                     = source_edge.edge_type.from_json(source_edge.json())
                new_graph.edges[edge_id] = new_edge