from typing                                                 import Set, Dict, Any, Type, Optional, Callable, List
from mgraph_db.mgraph.domain.Domain__MGraph__Node           import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_db.query.actions.MGraph__Query__Add import MGraph__Query__Add
from mgraph_db.query.actions.MGraph__Query__Navigate import MGraph__Query__Navigate
from mgraph_db.query.domain.Domain__MGraph__Query import Domain__MGraph__Query
from mgraph_db.query.models.Model__MGraph__Query__View      import Model__MGraph__Query__View
from mgraph_db.query.models.Model__MGraph__Query__Views     import Model__MGraph__Query__Views
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.Obj_Id                             import Obj_Id
from mgraph_db.mgraph.actions.MGraph__Data                  import MGraph__Data
from mgraph_db.mgraph.actions.MGraph__Index                 import MGraph__Index
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from osbot_utils.utils.Dev                                  import pprint

VIEW__OPERATION__INITIAL = 'initial'

class MGraph__Query(Type_Safe):
    mgraph_data  : MGraph__Data
    mgraph_index : MGraph__Index
    query_views  : Model__MGraph__Query__Views
    root_nodes   : Set[Obj_Id]

    def setup(self):
        source_nodes, source_edges = self.get_source_ids()              # get all the current nodes and edges
        self.create_view(nodes_ids = set()       ,                      # create a view for it which is the initial view
                         edges_ids = set()       ,
                         operation = 'initial'   ,
                         params    = {}          )
        return self

    @cache_on_self
    def query(self):
        return Domain__MGraph__Query(mgraph_data  = self.mgraph_data,
                                     mgraph_index = self.mgraph_index,
                                     query_views  = self.query_views ,
                                     root_nodes   = self.root_nodes  )

    @cache_on_self
    def navigate(self):
        return MGraph__Query__Navigate(query=self.query())

    @cache_on_self
    def add(self):
        return MGraph__Query__Add(query=self.query())

    # todo: refactor all the methods below into specific classes
    def export_view(self):
        from mgraph_db.query.actions.MGraph__Query__Export__View import MGraph__Query__Export__View
        export_view = MGraph__Query__Export__View(mgraph_query=self)
        mgraph_view = export_view.export()
        return mgraph_view

    def save_to_png(self, path, show_node__value:bool=True, show_source_graph=False):
        from mgraph_db.query.actions.MGraph__Query__Screenshot import MGraph__Query__Screenshot
        kwargs = dict(mgraph_query      = self             ,
                      show_node__value  = show_node__value ,
                      show_source_graph = show_source_graph)
        with MGraph__Query__Screenshot(**kwargs) as _:
            _.save_to(path)
            return _
    # def export(self):
    #     from mgraph_db.query.actions.MGraph__Query__Export__View import MGraph__Query__Export__View
    #     return MGraph__Query__Export__View(mgraph_query=self).export()

    def reset(self):
        self.query_views = Model__MGraph__Query__Views()
        self.setup()
        return self

    def get_source_ids(self) -> tuple[Set[Obj_Id], Set[Obj_Id]]:
        return (set(self.mgraph_data.nodes_ids()),
                set(self.mgraph_data.edges_ids()))

    def get_current_ids(self) -> tuple[Set[Obj_Id], Set[Obj_Id]]:
        current_view = self.query_views.current_view()
        # if not current_view:
        #     return self.get_source_ids()
        return (current_view.nodes_ids(),
                current_view.edges_ids())

    def get_connecting_edges(self, node_ids: Set[Obj_Id]) -> Set[Obj_Id]:
        edges = set()
        for node_id in node_ids:
            node           = self.mgraph_data.node(node_id)
            outgoing_edges = self.mgraph_index.get_node_outgoing_edges(node)
            incoming_edges = self.mgraph_index.get_node_incoming_edges(node)
            edges.update(outgoing_edges)
            edges.update(incoming_edges)
        return edges

    def create_view(self, nodes_ids: Set[Obj_Id],
                          edges_ids : Set[Obj_Id],
                          operation : str,
                          params    : Dict[str, Any]
                    )  -> Model__MGraph__Query__View:
        current_view = self.query_views.current_view()
        previous_id  = current_view.view_id() if current_view else None

        if self.in_initial_view() and nodes_ids:
            self.root_nodes = nodes_ids

        return self.query_views.add_view(nodes_ids   = nodes_ids  ,
                                         edges_ids   = edges_ids  ,
                                         operation   = operation  ,
                                         params      = params     ,
                                         previous_id = previous_id)

    def by_type(self, node_type: Type[Schema__MGraph__Node]) -> 'MGraph__Query':
        matching_ids = self.mgraph_index.get_nodes_by_type(node_type)
        current_nodes, current_edges = self.get_current_ids()

        filtered_nodes = matching_ids & current_nodes if current_nodes else matching_ids
        filtered_edges = self.get_connecting_edges(filtered_nodes)

        self.create_view(nodes_ids = filtered_nodes,
                         edges_ids = filtered_edges,
                         operation = 'by_type',
                         params    = {'type': node_type.__name__})
        return self

    def go_back(self) -> bool:
        current_view = self.query_views.current_view()
        if current_view and current_view.previous_view_id():
            return self.query_views.set_current_view(current_view.previous_view_id())
        return False

    def go_forward(self, view_id: Optional[Obj_Id] = None) -> bool:
        current_view = self.query_views.current_view()
        if not current_view:
            return False

        next_ids = current_view.next_view_ids()
        if not next_ids:
            return False

        if view_id:
            if view_id in next_ids:
                return self.query_views.set_current_view(view_id)
            return False

        return self.query_views.set_current_view(next(iter(next_ids)))

    def with_node_value(self, value: Any,
                              edge_type: Optional[Type[Schema__MGraph__Edge]] = None) -> 'MGraph__Query':           # Find nodes with specific value and optional edge type
        matching_ids = self.mgraph_index.get_nodes_connected_to_value(value=value, edge_type=edge_type)

        current_nodes, current_edges = self.get_current_ids()

        filtered_nodes = matching_ids & current_nodes if current_nodes else matching_ids
        filtered_edges = self.get_connecting_edges(filtered_nodes)

        self.create_view(nodes_ids = filtered_nodes,
                         edges_ids = filtered_edges,
                         operation = 'with_value',
                         params    = { 'value_type': type(value).__name__,
                                      'value': str(value)})
        return self

    # def with_field(self, name: str, value: Any) -> 'MGraph__Query':
    #     matching_ids = self.mgraph_index.get_nodes_by_field(name, value)               # Get matching nodes from index
    #
    #     current_nodes, current_edges = self.get_current_ids()                          # Get current state
    #
    #     new_nodes = matching_ids | current_nodes                                       # Merge with current nodes
    #
    #     self.create_view(nodes_ids = new_nodes,
    #                      edges_ids = current_edges,                                     # Keep current edges
    #                      operation = 'with_field',
    #                      params    = {'name': name, 'value': value})
    #     return self


    def index(self):
        return self.mgraph_index

    def re_index(self):
        self.mgraph_index = MGraph__Index.from_graph(self.mgraph_data.graph)                            # todo: check how this works with the new values_index

    def collect(self) -> List[Domain__MGraph__Node]:                                                    #  Returns list of all matching nodes in current view"""
        nodes_ids    = self.get_current_ids()[0]
        return [self.mgraph_data.node(node_id)
                for node_id in nodes_ids]

    def first(self) -> Optional[Domain__MGraph__Node]:                                                  # Returns first matching node or None"""
        nodes_ids = self.get_current_ids()[0]
        if nodes_ids:
            return self.mgraph_data.node(next(iter(nodes_ids)))
        return None

    def value(self) -> Optional[Any]:                                                                   # Returns value of first matching node or None
        first_node = self.first()
        return first_node.node_data.value if first_node else None

    def count(self) -> int:                                                                             # Returns count of matching nodes
        return len(self.get_current_ids()[0])

    def exists(self) -> bool:                                                                           # Returns whether any nodes match current query
        return bool(self.get_current_ids()[0])

    def current_view(self) -> Optional[Model__MGraph__Query__View]:                                     # Returns current view if any
        return self.query_views.current_view()

    def in_initial_view(self):
        current_view = self.current_view()
        return (current_view is None) or (self.current_view().query_operation() == VIEW__OPERATION__INITIAL)

    def traverse(self, edge_type: Optional[Type[Schema__MGraph__Edge]] = None) -> 'MGraph__Query':      # Traverses to connected nodes, optionally filtering by edge type"""
        current_nodes, _ = self.get_current_ids()
        connected_nodes = set()

        for node_id in current_nodes:
            # Get connecting edges
            edges = self.mgraph_index.get_node_outgoing_edges(
                self.mgraph_data.node(node_id))

            if edge_type:
                edges = {edge_id for edge_id in edges
                        if isinstance(self.mgraph_data.edge(edge_id), edge_type)}

            # Get connected nodes
            for edge_id in edges:
                edge = self.mgraph_data.edge(edge_id)                               # todo: double check this logic
                if edge.from_node_id == node_id:
                    connected_nodes.add(edge.to_node_id())
                else:
                    connected_nodes.add(edge.from_node_id())

        edges = self.get_connecting_edges(connected_nodes)

        self.create_view(nodes_ids = connected_nodes,
                        edges_ids = edges,
                        operation = 'traverse',
                        params    = {'edge_type': edge_type.__name__ if edge_type else None})
        return self


    def filter(self, predicate: Callable[[Domain__MGraph__Node], bool]) -> 'MGraph__Query': # Filters nodes using provided predicate function
        current_nodes, _ = self.get_current_ids()
        filtered_nodes = {
            node_id for node_id in current_nodes
            if predicate(self.mgraph_data.node(node_id))
        }

        filtered_edges = self.get_connecting_edges(filtered_nodes)

        self.create_view(nodes_ids = filtered_nodes,
                        edges_ids = filtered_edges,
                        operation = 'filter',
                        params    = {'predicate': str(predicate)})
        return self

    def print_stats(self):
        pprint(self.stats())

    def stats(self) -> Dict[str, Any]:
        source_nodes, source_edges   = self.get_source_ids()
        current_view                 = self.query_views.current_view()

        stats = { 'source_graph': { 'nodes': len(source_nodes),
                                    'edges': len(source_edges)},
                  'current_view' : current_view.stats()}
        return stats

    def edges_ids(self):
        current_view = self.query_views.current_view()
        return current_view.edges_ids()

    def nodes_ids(self):
        current_view = self.query_views.current_view()
        return current_view.nodes_ids()

    def add_outgoing_edges(self) -> 'MGraph__Query':                                        # Add outgoing edges to current view
        current_nodes, current_edges = self.get_current_ids()                               # Get current nodes and edges
        new_nodes = set()                                                                   # Initialize new node set
        new_edges = set()                                                                   # Initialize new edge set

        for node_id in current_nodes:                                                       # For each current node
            node = self.mgraph_data.node(node_id)                                           # Get the node
            if node:
                outgoing_edges = self.mgraph_index.get_node_outgoing_edges(node)            # Get outgoing edges
                new_edges.update(outgoing_edges)                                            # Add to new edges set

                for edge_id in outgoing_edges:                                              # For each outgoing edge
                    edge = self.mgraph_data.edge(edge_id)                                   # Get the edge
                    if edge:
                        new_nodes.add(edge.to_node_id())                                    # Add target node to new nodes

        combined_nodes = current_nodes | new_nodes                                          # Combine current and new nodes/edges
        combined_edges = current_edges | new_edges

        self.create_view(nodes_ids = combined_nodes,                                        # Create new view with combined sets
                         edges_ids = combined_edges,
                         operation = 'add_outgoing_edges',
                         params    = {})
        return

    def add_outgoing_edges__with_depth(self, depth:int)  -> 'MGraph__Query':
        for _ in range(0, depth):
            self.add_outgoing_edges()
        return self

    # def add_outgoing_edges__with_field(self, field_name: str) -> 'MGraph__Query':           # Add outgoing edges, but only for nodes with a specific field name
    #     current_nodes, current_edges = self.get_current_ids()                               # Get current state
    #     new_nodes = set()                                                                   # Initialize new sets
    #     new_edges = set()
    #
    #     matching_nodes = self.mgraph_index.get_nodes_by_field('name', field_name)          # Get nodes with matching field
    #
    #     for node_id in current_nodes:                                                       # For each current node
    #         node = self.mgraph_data.node(node_id)
    #         if node:
    #             outgoing_edges = self.mgraph_index.get_node_outgoing_edges(node)           # Get its outgoing edges
    #
    #             for edge_id in outgoing_edges:                                             # For each edge
    #                 edge = self.mgraph_data.edge(edge_id)
    #                 if edge:
    #                     target_node_id = edge.to_node_id()                                 # Get target node
    #                     if target_node_id in matching_nodes:                               # If target has matching field
    #                         new_edges.add(edge_id)                                         # Add the edge
    #                         new_nodes.add(target_node_id)                                  # Add the target node
    #
    #                         # Add value node connections
    #                         property_node = self.mgraph_data.node(target_node_id)
    #                         if property_node:
    #                             value_edges = self.mgraph_index.get_node_outgoing_edges(property_node)
    #                             for value_edge_id in value_edges:
    #                                 value_edge = self.mgraph_data.edge(value_edge_id)
    #                                 if value_edge:
    #                                     new_edges.add(value_edge_id)                       # Add the value edge
    #                                     new_nodes.add(value_edge.to_node_id())
    #
    #     combined_nodes = current_nodes | new_nodes                                         # Combine sets
    #     combined_edges = current_edges | new_edges
    #
    #     self.create_view(nodes_ids = combined_nodes,                                       # Create new view
    #                     edges_ids = combined_edges,
    #                     operation = 'add_outgoing_edges_with_field',
    #                     params    = {'field_name': field_name})
    #     return self

    def add_node_id(self, node_id: Obj_Id) -> 'MGraph__Query':                                      # Add specific node to view

        current_nodes, current_edges = self.get_current_ids()                                       # Get current nodes and edges

        if not self.mgraph_data.node(node_id):                                                      # Validate node exists
            return self

        new_nodes = current_nodes | {node_id}                                                       # Add new node to set
        new_edges = current_edges                                                                   # Start with current edges


        self.create_view(nodes_ids = new_nodes,
                         edges_ids = new_edges,
                         operation = 'add_node_id',
                         params    = {'node_id': str(node_id)})                                     # Create new view with added node
        return self

    def add_nodes_ids(self, nodes_ids: Set[Obj_Id]) -> 'MGraph__Query':  # Add multiple nodes to view
        current_nodes, current_edges = self.get_current_ids()  # Get current nodes and edges

        # Filter out any invalid node IDs
        valid_nodes = {node_id for node_id in nodes_ids
                       if self.mgraph_data.node(node_id)}  # Validate nodes exist

        if not valid_nodes:  # Return if no valid nodes
            return self

        new_nodes = current_nodes | valid_nodes  # Add new nodes to set
        new_edges = current_edges  # Start with current edges

        self.create_view(nodes_ids=new_nodes,
                         edges_ids=new_edges,
                         operation='add_nodes_ids',
                         params={'nodes_ids': [str(node_id) for node_id in
                                               valid_nodes]})  # Create new view with added nodes
        return self
