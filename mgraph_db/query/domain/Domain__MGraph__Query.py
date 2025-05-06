from typing import Type, Set, Dict, Any

from mgraph_db.query.models.Model__MGraph__Query__View import Model__MGraph__Query__View

from mgraph_db.mgraph.actions.MGraph__Data               import MGraph__Data
from mgraph_db.mgraph.actions.MGraph__Index              import MGraph__Index
from mgraph_db.query.models.Model__MGraph__Query__Views  import Model__MGraph__Query__Views
from osbot_utils.helpers.Obj_Id                          import Obj_Id
from osbot_utils.type_safe.Type_Safe                     import Type_Safe


class Domain__MGraph__Query(Type_Safe):
    mgraph_index: MGraph__Index                 = None                               # Access to graph index
    mgraph_data : MGraph__Data                  = None
    query_views : Model__MGraph__Query__Views                                        # Query view management
    query_type  : Type['Domain__MGraph__Query']                                      # Self type reference
    root_nodes  : Set[Obj_Id]

    def setup(self):
        if self.mgraph_data is None:
            raise ValueError("in Domain__MGraph__Query, the self.mgraph_data was not set")
        if self.mgraph_index is None:
            raise ValueError("in Domain__MGraph__Query, the self.mgraph_index was not set")
        self.query_views = Model__MGraph__Query__Views()                             # Initialize views
        return self.create_initial_view()

    def create_initial_view(self):                                                   # Create empty initial view
        self.query_views.add_view(nodes_ids = set()    ,
                                 edges_ids = set()    ,
                                 operation = 'initial',
                                 params    = {}       )
        return self

    def current_view(self):                                                         # Get current query view
        return self.query_views.current_view()

    def get_current_ids(self) -> tuple[set[Obj_Id], set[Obj_Id]]:                  # Get current nodes and edges
        current_view = self.current_view()
        if not current_view:
            return set(), set()
        return (current_view.nodes_ids(),
                current_view.edges_ids())

    def get_connecting_edges(self, node_ids: set[Obj_Id]) -> set[Obj_Id]:          # Get edges connecting nodes
        edges = set()
        for node_id in node_ids:
            outgoing_edges = self.mgraph_index.get_node_id_outgoing_edges(node_id)
            incoming_edges = self.mgraph_index.get_node_id_incoming_edges(node_id)
            if outgoing_edges:
                edges.update(outgoing_edges)
            if incoming_edges:
                edges.update(incoming_edges)
        return edges

    # def create_view(self, nodes_ids: set[Obj_Id],                                   # Create new query view
    #                       edges_ids : set[Obj_Id],
    #                       operation : str,
    #                       params    : dict) -> None:
    #     current_view = self.current_view()
    #     previous_id  = current_view.view_id() if current_view else None
    #
    #     self.query_views.add_view(nodes_ids   = nodes_ids ,
    #                               edges_ids    = edges_ids ,
    #                               operation    = operation ,
    #                               params       = params    ,
    #                               previous_id  = previous_id)
    #     return self

    def create_view(self, nodes_ids : Set[Obj_Id],
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

    def in_initial_view(self) -> bool:                                             # Check if in initial view
        current_view = self.current_view()
        return (current_view is None) or (current_view.query_operation() == 'initial')