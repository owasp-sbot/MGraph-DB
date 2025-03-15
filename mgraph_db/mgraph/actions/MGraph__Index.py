from typing                                               import Type, Set, Any, Dict, Optional
from mgraph_db.mgraph.actions.MGraph__Index__Values       import MGraph__Index__Values
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value import Schema__MGraph__Node__Value
from osbot_utils.helpers.Safe_Id                          import Safe_Id
from osbot_utils.utils.Dev                                import pprint
from mgraph_db.mgraph.domain.Domain__MGraph__Graph        import Domain__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node        import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge        import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Index__Data import Schema__MGraph__Index__Data
from osbot_utils.helpers.Obj_Id                           import Obj_Id
from osbot_utils.type_safe.Type_Safe                      import Type_Safe
from osbot_utils.utils.Json                               import json_file_create, json_load_file

class MGraph__Index(Type_Safe):
    index_data  : Schema__MGraph__Index__Data
    values_index: MGraph__Index__Values

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    # todo: refactor all these add_* methods to an MGraph__Index__Create class (which will hold all the logic to create the index)
    #       the main methods in this class should be focused on easy access to the MGraph index data
    def add_node(self, node: Schema__MGraph__Node) -> None:                         # Add a node to the index
        node_id   = node.node_id
        node_type = node.node_type.__name__

        self.index_data.nodes_types[node_id] = node_type

        if node_id not in self.index_data.nodes_to_outgoing_edges:                  # Initialize sets if needed
            self.index_data.nodes_to_outgoing_edges[node_id] = set()
        if node_id not in self.index_data.nodes_to_incoming_edges:
            self.index_data.nodes_to_incoming_edges[node_id] = set()

        if node_type not in self.index_data.nodes_by_type:                          # Add to type index
            self.index_data.nodes_by_type[node_type] = set()
        self.index_data.nodes_by_type[node_type].add(node_id)

        if node.node_type and issubclass(node.node_type, Schema__MGraph__Node__Value):                           # if the data is a value
            self.values_index.add_value_node(node)                        # add it to the index



    def add_edge(self, edge: Schema__MGraph__Edge) -> None:                     # Add an edge to the index
        edge_id      = edge.edge_id
        from_node_id = edge.from_node_id
        to_node_id   = edge.to_node_id
        edge_type    = edge.edge_type.__name__

        self.add_edge_label(edge)

        self.index_data.edges_types   [edge_id] = edge_type
        self.index_data.edges_to_nodes[edge_id] = (from_node_id, to_node_id)


        if edge_type not in self.index_data.edges_by_type:                                         # Add to type index
            self.index_data.edges_by_type[edge_type] = set()
        self.index_data.edges_by_type[edge_type].add(edge_id)

        if to_node_id not in self.index_data.nodes_to_incoming_edges_by_type:                       # Update the new nodes_to_incoming_edges_by_type
            self.index_data.nodes_to_incoming_edges_by_type[to_node_id] = {}
        if edge_type not in self.index_data.nodes_to_incoming_edges_by_type[to_node_id]:
            self.index_data.nodes_to_incoming_edges_by_type[to_node_id][edge_type] = set()
        self.index_data.nodes_to_incoming_edges_by_type[to_node_id][edge_type].add(edge_id)


        if from_node_id not in self.index_data.nodes_to_outgoing_edges_by_type:                     # Update the nodes_to_outgoing_edges_by_type index
            self.index_data.nodes_to_outgoing_edges_by_type[from_node_id] = {}
        if edge_type not in self.index_data.nodes_to_outgoing_edges_by_type[from_node_id]:
            self.index_data.nodes_to_outgoing_edges_by_type[from_node_id][edge_type] = set()
        self.index_data.nodes_to_outgoing_edges_by_type[from_node_id][edge_type].add(edge_id)

        if from_node_id not in self.index_data.nodes_to_outgoing_edges:                              # Add to node relationship indexes
            self.index_data.nodes_to_outgoing_edges[from_node_id] = set()
        self.index_data.nodes_to_outgoing_edges[from_node_id].add(edge_id)
        if to_node_id not in self.index_data.nodes_to_incoming_edges:
            self.index_data.nodes_to_incoming_edges[to_node_id] = set()
        self.index_data.nodes_to_incoming_edges[to_node_id].add(edge_id)


    def add_edge_label(self, edge) -> None:
        if edge.edge_label:
            edge_id = edge.edge_id

            if edge.edge_label.predicate:                                   # Index by predicate
                predicate = edge.edge_label.predicate
                self.index_data.edges_predicates[edge_id] = predicate       # Store edge_id to predicate mapping

                if predicate not in self.index_data.edges_by_predicate:     # Store predicate to edge_id mapping
                    self.index_data.edges_by_predicate[predicate] = set()
                self.index_data.edges_by_predicate[predicate].add(edge_id)

            if edge.edge_label.incoming:                                    # Index by incoming label
                incoming = edge.edge_label.incoming
                if incoming not in self.index_data.edges_by_incoming_label:
                    self.index_data.edges_by_incoming_label[incoming] = set()
                self.index_data.edges_by_incoming_label[incoming].add(edge_id)

            if edge.edge_label.outgoing:                                    # Index by outgoing label
                outgoing = edge.edge_label.outgoing
                if outgoing not in self.index_data.edges_by_outgoing_label:
                    self.index_data.edges_by_outgoing_label[outgoing] = set()
                self.index_data.edges_by_outgoing_label[outgoing].add(edge_id)

    def remove_node(self, node: Schema__MGraph__Node) -> None:  # Remove a node and all its references from the index"""
        node_id = node.node_id

        # Get associated edges before removing node references
        outgoing_edges = self.index_data.nodes_to_outgoing_edges.pop(node_id, set())
        incoming_edges = self.index_data.nodes_to_incoming_edges.pop(node_id, set())

        # Remove from type index
        node_type = node.node_type.__name__
        if node_type in self.index_data.nodes_by_type:
            self.index_data.nodes_by_type[node_type].discard(node_id)
            if not self.index_data.nodes_by_type[node_type]:
                del self.index_data.nodes_by_type[node_type]

        if node.node_data is Schema__MGraph__Node__Value:                               # if the data is a value
            self.values_index.remove_value_node(node.node_data)                         # remove it from the index



    def remove_edge(self, edge: Schema__MGraph__Edge) -> None:          # Remove an edge and all its references from the index
        edge_id = edge.edge_id

        self.remove_edge_label(edge)

        if edge_id in self.index_data.edges_to_nodes:
            from_node_id, to_node_id = self.index_data.edges_to_nodes.pop(edge_id)
            self.index_data.nodes_to_outgoing_edges[from_node_id].discard(edge_id)
            self.index_data.nodes_to_incoming_edges[to_node_id].discard(edge_id)

            if to_node_id in self.index_data.nodes_to_incoming_edges_by_type:
                edge_type = edge.edge_type.__name__
                if edge_type in self.index_data.nodes_to_incoming_edges_by_type[to_node_id]:
                    self.index_data.nodes_to_incoming_edges_by_type[to_node_id][edge_type].discard(edge_id)
                    if not self.index_data.nodes_to_incoming_edges_by_type[to_node_id][edge_type]:
                        del self.index_data.nodes_to_incoming_edges_by_type[to_node_id][edge_type]
                if not self.index_data.nodes_to_incoming_edges_by_type[to_node_id]:
                    del self.index_data.nodes_to_incoming_edges_by_type[to_node_id]

        # Remove from type index
        edge_type = edge.edge_type.__name__
        if edge_type in self.index_data.edges_by_type:
            self.index_data.edges_by_type[edge_type].discard(edge_id)
            if not self.index_data.edges_by_type[edge_type]:
                del self.index_data.edges_by_type[edge_type]

    def remove_edge_label(self, edge) -> None:
        edge_id = edge.edge_id

        if edge.edge_label and edge.edge_label.predicate:                           # Remove from predicate indexes
            predicate = edge.edge_label.predicate
            if predicate in self.index_data.edges_by_predicate:
                self.index_data.edges_by_predicate[predicate].discard(edge_id)
                if not self.index_data.edges_by_predicate[predicate]:
                    del self.index_data.edges_by_predicate[predicate]

            if edge_id in self.index_data.edges_predicates:
                del self.index_data.edges_predicates[edge_id]

        if edge.edge_label and edge.edge_label.incoming:                            # Remove from incoming label index
            incoming = edge.edge_label.incoming
            if incoming in self.index_data.edges_by_incoming_label:
                self.index_data.edges_by_incoming_label[incoming].discard(edge_id)
                if not self.index_data.edges_by_incoming_label[incoming]:
                    del self.index_data.edges_by_incoming_label[incoming]

        if edge.edge_label and edge.edge_label.outgoing:                            # Remove from outgoing label index
            outgoing = edge.edge_label.outgoing
            if outgoing in self.index_data.edges_by_outgoing_label:
                self.index_data.edges_by_outgoing_label[outgoing].discard(edge_id)
                if not self.index_data.edges_by_outgoing_label[outgoing]:
                    del self.index_data.edges_by_outgoing_label[outgoing]



    # todo: see if we need this capability (which is to store in the index the data from the edge's data).
    #       I removed it becasue there was no use that needed this
    # def index_edge_data(self, edge: Schema__MGraph__Edge) -> None:
    #     """Index all fields from edge_data"""
    #     if edge.edge_data:
    #         for field_name, field_value in edge.edge_data.__dict__.items():
    #             if field_name.startswith('_'):
    #                 continue
    #             if field_name not in self.index_data.edges_by_field:
    #                 self.index_data.edges_by_field[field_name] = {}
    #             if field_value not in self.index_data.edges_by_field[field_name]:
    #                 self.index_data.edges_by_field[field_name][field_value] = set()
    #             self.index_data.edges_by_field[field_name][field_value].add(edge.edge_id)

    # def remove_edge_data(self, edge: Schema__MGraph__Edge) -> None:
    #     """Remove indexed edge_data fields"""
    #     if edge.edge_data:
    #         for field_name, field_value in edge.edge_data.__dict__.items():
    #             if field_name.startswith('_'):
    #                 continue
    #             if field_name in self.index_data.edges_by_field:
    #                 if field_value in self.index_data.edges_by_field[field_name]:
    #                     self.index_data.edges_by_field[field_name][field_value].discard(edge.edge_id)

    def load_index_from_graph(self, graph : Domain__MGraph__Graph) -> None:                                             # Create index from existing graph
        for node_id, node in graph.model.data.nodes.items():                                                            # Add all nodes to index
            self.add_node(node)

        for edge_id, edge in graph.model.data.edges.items():                                           # Add all edges to index
            self.add_edge(edge)

    def print__index_data(self):
        index_data = self.index_data.json()
        pprint(index_data)
        return index_data

    def print__stats(self):
        stats = self.stats()
        pprint(stats)
        return stats

    def save_to_file(self, target_file: str) -> None:                                               # Save index to file
        index_data = self.index_data.json()                                                              # get json (serialised) representation of the index object
        return json_file_create(index_data, target_file)                                            # save it to the target file

    def stats(self) -> Dict[str, Any]:                                                    # Returns statistical summary of index data
        edge_counts = {                                                                                   # Calculate total edges per node
            node_id: {
                'incoming': len(self.index_data.nodes_to_incoming_edges.get(node_id, [])),
                'outgoing': len(self.index_data.nodes_to_outgoing_edges.get(node_id, []))
            }
            for node_id in set(self.index_data.nodes_to_incoming_edges.keys()) |
                           set(self.index_data.nodes_to_outgoing_edges.keys())
        }
        avg_incoming_edges = sum(n['incoming'] for n in edge_counts.values()) / len(edge_counts) if edge_counts else 0
        avg_outgoing_edges = sum(n['outgoing'] for n in edge_counts.values()) / len(edge_counts) if edge_counts else 0
        stats_data = {                                                                                   # Initialize stats dictionary
            'index_data': {
                'edge_to_nodes'          : len(self.index_data.edges_to_nodes)          ,                # Count of edge to node mappings
                'edges_by_type'          : {k: len(v) for k,v in                                        # Count of edges per type
                                          self.index_data.edges_by_type.items()}        ,
                'nodes_by_type'          : {k: len(v) for k,v in                                        # Count of nodes per type
                                          self.index_data.nodes_by_type.items()}        ,
                'node_edge_connections'   : {                                                           # Consolidated edge counts
                    'total_nodes'        : len(edge_counts)                            ,
                    'avg_incoming_edges' : round(avg_incoming_edges),
                    'avg_outgoing_edges' : round(avg_outgoing_edges),
                    'max_incoming_edges' : max((n['incoming'] for n in edge_counts.values()), default=0),
                    'max_outgoing_edges' : max((n['outgoing'] for n in edge_counts.values()), default=0)
                }
            }
        }

        return stats_data

    # todo: refactor all methods above to MGraph__Index__Create


    ##### getters for data
    # todo refactor this to names like edges__from__node , nodes_from_node

    def get_edge_predicate(self, edge_id: Obj_Id):
        return self.index_data.edges_predicates.get(edge_id)

    def get_nodes_connected_to_value(self, value     : Any ,
                                           edge_type : Type[Schema__MGraph__Edge       ] = None ,
                                           node_type : Type[Schema__MGraph__Node__Value] = None
                                      ) -> Set[Obj_Id]:                                             # Get nodes connected to a value node through optional edge type
        value_type = type(value)
        if node_type is None:
            node_type = Schema__MGraph__Node__Value
        node_id    = self.values_index.get_node_id_by_value(value_type=value_type, value=value, node_type=node_type)     # Find value node
        if not node_id:                                                                                                 # No matching value found
            return set()

        connected_nodes = set()                                                                     # Find nodes connected to this value node through edges
        incoming_edges =  self.index_data.nodes_to_incoming_edges.get(node_id, set())

        if edge_type:                                                                               # If edge type specified
            edge_type_name = edge_type.__name__
            filtered_edges = set()
            for edge_id in incoming_edges:
                if self.index_data.edges_types[edge_id] == edge_type_name:                          # Filter edges by type
                    filtered_edges.add(edge_id)
            incoming_edges = filtered_edges

        for edge_id in incoming_edges:                                                              # Get nodes pointing to this value
            from_node_id, _ = self.edges_to_nodes()[edge_id]
            connected_nodes.add(from_node_id)

        return connected_nodes

    def get_node_connected_to_node__outgoing(self, node_id: Obj_Id, edge_type: str) -> Optional[Obj_Id]:
        connected_edges = self.index_data.nodes_to_outgoing_edges_by_type.get(node_id, {}).get(edge_type, set())

        if connected_edges:
            edge_id = next(iter(connected_edges))                                                   # Get the first edge ID from the set
            from_node_id, to_node_id = self.index_data.edges_to_nodes.get(edge_id, (None, None))     # Retrieve the connected node IDs from the edge_to_nodes mapping
            return to_node_id

        return None

    def get_node_outgoing_edges(self, node: Schema__MGraph__Node) -> Set[Obj_Id]:           # Get all outgoing edges for a node
        return self.index_data.nodes_to_outgoing_edges.get(node.node_id, set())

    def get_node_id_outgoing_edges(self, node_id: Obj_Id) -> Set[Obj_Id]:           # Get all outgoing edges for a node
        return self.index_data.nodes_to_outgoing_edges.get(node_id, set())

    def get_node_id_incoming_edges(self, node_id: Obj_Id) -> Set[Obj_Id]:           # Get all incoming edges for a node
        return self.index_data.nodes_to_incoming_edges.get(node_id, set())

    def get_node_incoming_edges(self, node: Schema__MGraph__Node) -> Set[Obj_Id]:           # Get all incoming edges for a node
        return self.index_data.nodes_to_incoming_edges.get(node.node_id, set())

    def get_nodes_by_type(self, node_type: Type[Schema__MGraph__Node]) -> Set[Obj_Id]:      # Get all nodes of a specific type
        return self.index_data.nodes_by_type.get(node_type.__name__, set())

    def get_edges_by_type(self, edge_type: Type[Schema__MGraph__Edge]) -> Set[Obj_Id]:      # Get all edges of a specific type
        return self.index_data.edges_by_type.get(edge_type.__name__, set())

    #### helpers for edge's labels # todo: look at refactoring these getters into a helper class
    def get_edges_by_predicate(self, predicate : Safe_Id) -> Set[Obj_Id]: # Get all edges with specific predicate
        return self.index_data.edges_by_predicate.get(predicate, set())


    def get_edges_by_incoming_label(self, label : Safe_Id) -> Set[Obj_Id]:# Get edges with specific incoming label
        return self.index_data.edges_by_incoming_label.get(label, set())

    def get_edges_by_outgoing_label(self, label : Safe_Id) -> Set[Obj_Id]: # Get edges with specific outgoing label
        return self.index_data.edges_by_outgoing_label.get(label, set())


    def get_node_outgoing_edges_by_predicate(self, node_id  : Obj_Id  ,     # Node to get edges from
                                                   predicate: Safe_Id       # Predicate to filter by
                                              ) -> Set[Obj_Id]:
        outgoing_edges  = self.get_node_id_outgoing_edges(node_id)
        predicate_edges = self.get_edges_by_predicate(predicate)
        return outgoing_edges.intersection(predicate_edges)


    def get_node_incoming_edges_by_predicate(self, node_id  : Obj_Id  ,     # Node to get edges to
                                                   predicate: Safe_Id       # Predicate to filter by
                                              ) -> Set[Obj_Id]:
        incoming_edges  = self.get_node_id_incoming_edges(node_id)
        predicate_edges = self.get_edges_by_predicate(predicate)
        return incoming_edges.intersection(predicate_edges)


    def get_nodes_by_predicate(self, from_node_id: Obj_Id  ,                # Source node
                                     predicate   : Safe_Id                  # Predicate to traverse
                                ) -> Set[Obj_Id]:                           # Returns target nodes
        edge_ids = self.get_node_outgoing_edges_by_predicate(from_node_id, predicate)
        result = set()
        for edge_id in edge_ids:
            _, to_node_id = self.index_data.edges_to_nodes.get(edge_id, (None, None))
            if to_node_id:
                result.add(to_node_id)
        return result

    # todo: refactor this to something like raw__edges_to_nodes , ...
    #       in fact once we add the main helper methods (like edges_ids__from__node_id) see if these methods are still needed
    def edges_to_nodes                 (self): return self.index_data.edges_to_nodes
    def edges_by_type                  (self): return self.index_data.edges_by_type
    def nodes_by_type                  (self): return self.index_data.nodes_by_type
    def nodes_to_incoming_edges        (self): return self.index_data.nodes_to_incoming_edges
    def nodes_to_incoming_edges_by_type(self): return self.index_data.nodes_to_incoming_edges_by_type
    def nodes_to_outgoing_edges        (self): return self.index_data.nodes_to_outgoing_edges
    def nodes_to_outgoing_edges_by_type(self): return  self.index_data.nodes_to_outgoing_edges_by_type

    # todo: create this @as_list decorator which converts the return value set to a list (see if that is the better name)
    # @set_to_list
    def edges_ids__from__node_id(self, node_id) -> list:
        with self.index_data as _:
            return list(_.nodes_to_outgoing_edges.get(node_id, {}))         # convert set to list

    def edges_ids__to__node_id(self, node_id) -> list:
        with self.index_data as _:
            return list(_.nodes_to_incoming_edges.get(node_id, {}))         # convert set to list

    def nodes_ids__from__node_id(self, node_id) -> list:
        with self.index_data as _:
            nodes_ids = []
            for edge_id in self.edges_ids__from__node_id(node_id):
                (from_node_id, to_node_id) = _.edges_to_nodes[edge_id]
                nodes_ids.append(to_node_id)
            return nodes_ids

    # todo: see there is a better place to put these static methods (or if we need them to be static)
    @classmethod
    def from_graph(cls, graph: Domain__MGraph__Graph) -> 'MGraph__Index':                           # Create index from graph
        with cls() as _:
            _.load_index_from_graph(graph)                                                             # Build initial index
            return _

    @classmethod
    def from_file(cls, source_file: str) -> 'MGraph__Index':                                           # Load index from file
        with cls() as _:
            index_data   = json_load_file(source_file)
            _.index_data = Schema__MGraph__Index__Data.from_json(index_data)
            return _
