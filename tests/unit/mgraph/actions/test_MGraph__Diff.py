from unittest                                                   import TestCase
from mgraph_db.mgraph.MGraph                                    import MGraph
from mgraph_db.mgraph.domain.Domain__MGraph__Node               import Domain__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Graph               import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Diff              import Schema__MGraph__Node__Changes, Schema__MGraph__Edge__Changes
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge              import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node              import Schema__MGraph__Node
from mgraph_db.mgraph.actions.MGraph__Diff                      import MGraph__Diff
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data        import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value       import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data import Schema__MGraph__Node__Value__Data
from osbot_utils.testing.__                                     import __
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
from osbot_utils.utils.Objects                                  import type_full_name



class test_MGraph__Diff(TestCase):

    def setUp(self):
        self.graph_a = MGraph()
        self.graph_b = MGraph()

    def test_compare_identical_graphs(self):
        mgraph_diff  = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        diff = mgraph_diff.diff_graphs()

        assert diff.obj() == __(nodes_added      = []  ,
                                nodes_removed    = []  ,
                                nodes_modified   = __(),
                                edges_added      = []  ,
                                edges_removed    = []  ,
                                edges_modified   = __(),
                                nodes_count_diff = 0   ,
                                edges_count_diff = 0   )


    def test_compare_different_nodes(self):

        with self.graph_a.edit() as edit_a:                                             # Add a node to graph A
            node_a = edit_a.new_node()

        with self.graph_b.edit() as edit_b:                                             # Add a different node to graph B
            node_b = edit_b.new_node()

        diff = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats = diff.diff_graphs()

        assert node_b.node_id in stats.nodes_added
        assert node_a.node_id in stats.nodes_removed
        assert stats.nodes_count_diff == 0  # Same number of nodes

        assert stats.obj() == __(nodes_added      = [node_b.node_id],
                                 nodes_removed    = [node_a.node_id],
                                 nodes_modified   = __(),
                                 edges_added      = []  ,
                                 edges_removed    = []  ,
                                 edges_modified   = __(),
                                 nodes_count_diff = 0   ,
                                 edges_count_diff = 0   )

    def test_compare_modified_node(self):
        class NodeA(Schema__MGraph__Node): pass
        class NodeB(Schema__MGraph__Node): pass

        with self.graph_a.edit() as edit_a:
            node_a = edit_a.new_node(node_type=NodeA)

        with self.graph_b.edit() as edit_b:
            node_b = edit_b.new_node(node_type=NodeB, node_id=node_a.node_id)

        diff  = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats = diff.diff_graphs()

        assert node_b.node_id == node_a.node_id
        assert stats.json()   == { 'edges_added'        : [],
                                   'edges_count_diff'   : 0,
                                   'edges_modified'     : {},
                                   'edges_removed'      : [],
                                   'nodes_added'        : [],
                                   'nodes_count_diff'   : 0,
                                   'nodes_modified'     : { str(node_a.node_id): {'data'    : None                                     ,
                                                                                  'type'    : {'from_value': 'test_MGraph__Diff.NodeA' ,
                                                                                               'to_value'  : 'test_MGraph__Diff.NodeB'}}},
                                 'nodes_removed': []}

    def test_compare_edges(self):
        class CustomEdge(Schema__MGraph__Edge): pass                                # Create custom edge type

        node_a1_id = "00000000"
        node_a2_id = "11111111"
        edge_a_id  = "88888888"
        edge_b_id  = "99999999"
        with self.graph_a.edit() as edit_a:                                         # Setup graph A
            node_a1 = edit_a.new_node(node_id=node_a1_id, node_type=Schema__MGraph__Node)
            node_a2 = edit_a.new_node(node_id=node_a2_id, node_type=Schema__MGraph__Node)
            edge_a  = edit_a.new_edge(edge_id      = edge_a_id              ,
                                      from_node_id = node_a1.node_id        ,
                                      to_node_id   = node_a2.node_id        ,
                                      edge_type    = Schema__MGraph__Edge   ).set_edge_type()

        with self.graph_b.edit() as edit_b:                                         # Setup graph B with same nodes but different edge
            node_b1 = edit_b.new_node(node_id      = node_a1.node_id, node_type=Schema__MGraph__Node)
            node_b2 = edit_b.new_node(node_id      = node_a2.node_id, node_type=Schema__MGraph__Node)
            edge_b  = edit_b.new_edge(edge_id      = edge_b_id       ,
                                      from_node_id = node_b1.node_id ,
                                      to_node_id   = node_b2.node_id ,
                                      edge_type    = CustomEdge      ).set_edge_type()
        assert node_a1.node_id == node_a1_id
        assert node_a2.node_id == node_a2_id
        assert node_b1.node_id == node_a1_id
        assert node_b2.node_id == node_a2_id
        assert edge_a.edge_id  == edge_a_id
        assert edge_b.edge_id  == edge_b_id



        diff  = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats = diff.diff_graphs()
        assert stats.obj() ==__(nodes_added=[],
                                nodes_removed=[],
                                nodes_modified=__(),
                                edges_added=['99999999'],
                                edges_removed=['88888888'],
                                edges_modified=__(),
                                nodes_count_diff=0,
                                edges_count_diff=0)

        assert self.graph_a.graph.model.data.nodes[node_a1.node_id].obj() == self.graph_b.graph.model.data.nodes[node_a1.node_id].obj()
        assert self.graph_a.graph.model.data.nodes[node_a2.node_id].obj() == self.graph_b.graph.model.data.nodes[node_a2.node_id].obj()

        assert edge_a.edge_id in stats.edges_removed
        assert edge_b.edge_id in stats.edges_added
        assert stats.json() == { 'edges_added'      : [edge_b.edge_id],
                                 'edges_count_diff' : 0,
                                 'edges_modified'   : {},
                                 'edges_removed'    : [edge_a.edge_id],
                                 'nodes_added'      : [],
                                 'nodes_count_diff' : 0,
                                 'nodes_modified'   : {},
                                 'nodes_removed'    : []}


    def test_node_data_changes(self):
        class CustomNodeData(Schema__MGraph__Node__Data):                                    # Create custom node types with data
            field_1: str
            field_2: int

        class CustomNode(Schema__MGraph__Node):
            node_data: CustomNodeData

        with self.graph_a.edit() as edit_a:                                                 # Add node with data to both graphs
            node_a = edit_a.new_node(node_type = CustomNode    ,
                                    field_1   = "original"    ,
                                    field_2   = 42           )

        with self.graph_b.edit() as edit_b:
            node_b = edit_b.new_node(node_type = CustomNode       ,                         # Changed field_1, same field_2
                                     node_id   = node_a.node_id   ,
                                     field_1   = "modified"       ,
                                     field_2   = 42              )

        diff    = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats   = diff.diff_graphs()
        changes = diff.compare_node_data(node_a.node_id)

        assert node_a.node_id in stats.nodes_modified
        assert changes.obj() == __(data=__(from_value =__(field_1='original'),
                                           to_value   =__(field_1='modified')),
                                           type       = None)

    def test_value_node_changes(self):
        with self.graph_a.edit() as edit_a:                                                  # Create value nodes with different values
            value_data_a = Schema__MGraph__Node__Value__Data(value      = "original_value"           ,
                                                             value_type = str                        )
            node_a       = edit_a.new_node                  (node_type  = Schema__MGraph__Node__Value,
                                                             node_data  = value_data_a               )
            node_a_id    = node_a.node_id

        assert type(node_a          ) is Domain__MGraph__Node
        assert type(node_a.node_data) is Schema__MGraph__Node__Value__Data
        assert node_a.node_type       is Schema__MGraph__Node__Value
        assert type(node_a.graph)     is Model__MGraph__Graph
        assert node_a.graph           == self.graph_a.graph.model
        assert node_a.graph           == edit_a.graph.model
        assert node_a.node.obj()     == __(data=__(node_data = __(value_type = 'builtins.str'  ,
                                                                   value      = 'original_value',
                                                                   key        = ''              ),
                                                    node_id   = node_a_id,
                                                    node_type = type_full_name(Schema__MGraph__Node__Value)))


        with self.graph_b.edit() as edit_b:
            value_data_b = Schema__MGraph__Node__Value__Data(value      = "new_value"                ,
                                                             value_type = str                        )
            node_b       = edit_b.new_node                  (node_type  = Schema__MGraph__Node__Value,
                                                             node_id    = node_a.node_id             ,
                                                             node_data  = value_data_b               )
            node_b_id    = node_b.node_id

        diff    = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats   = diff.diff_graphs()
        assert node_a_id    == node_b_id
        assert stats.json() == { 'edges_added'      : [],
                                 'edges_count_diff' : 0,
                                 'edges_modified'   : {},
                                 'edges_removed'    : [],
                                 'nodes_added'      : [],
                                 'nodes_count_diff' : 0,
                                 'nodes_modified'   : { str(node_a_id): { 'data': { 'from_value': { 'value'     : 'original_value'},
                                                                                    'to_value'  : { 'value'     : 'new_value'     }},
                                                                          'type': None}},
                                 'nodes_removed': []}

        changes = diff.compare_node_data(node_a.node_id)
        assert changes        != {}                                # BUG (and the ones below)
        assert node_a.node_id in stats.nodes_modified
        assert changes.obj()  ==__(data = __( from_value =__(value='original_value'),
                                              to_value   =__(value='new_value'     )),
                                   type = None)

    def test_edge_connection_changes(self):
        with self.graph_a.edit() as edit_a:
            node_a1 = edit_a.new_node()
            node_a2 = edit_a.new_node()
            node_a3 = edit_a.new_node()
            edge_a  = edit_a.new_edge(from_node_id=node_a1.node_id,
                                     to_node_id=node_a2.node_id)

        with self.graph_b.edit() as edit_b:
            node_b1 = edit_b.new_node(node_id=node_a1.node_id)
            node_b2 = edit_b.new_node(node_id=node_a2.node_id)
            node_b3 = edit_b.new_node(node_id=node_a3.node_id)
            edge_b  = edit_b.new_edge(edge_id=edge_a.edge_id,
                                     from_node_id=node_b1.node_id,
                                     to_node_id=node_b3.node_id)

        diff    = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats   = diff.diff_graphs()
        changes = stats.edges_modified[edge_a.edge_id]

        assert edge_a.edge_id in stats.edges_modified
        assert changes.type is None  # No type change
        assert changes.from_node is None  # No from_node change
        assert changes.to_node.obj() == __(from_value = node_a2.node_id,
                                           to_value   = node_b3.node_id)

    def test_edge_type_changes(self):
        class EdgeTypeA(Schema__MGraph__Edge): pass
        class EdgeTypeB(Schema__MGraph__Edge): pass

        with self.graph_a.edit() as edit_a:
            node_a1 = edit_a.new_node()
            node_a2 = edit_a.new_node()
            edge_a  = edit_a.new_edge(from_node_id = node_a1.node_id,
                                      to_node_id   = node_a2.node_id,
                                      edge_type    = EdgeTypeA      )

        with self.graph_b.edit() as edit_b:
            node_b1 = edit_b.new_node(node_id       = node_a1.node_id)
            node_b2 = edit_b.new_node(node_id       = node_a2.node_id)
            edge_b  = edit_b.new_edge(edge_id       = edge_a.edge_id ,
                                      from_node_id  = node_b1.node_id,
                                      to_node_id    = node_b2.node_id,
                                      edge_type     = EdgeTypeB      )

        diff    = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats   = diff.diff_graphs()
        changes = stats.edges_modified[edge_a.edge_id]

        assert edge_a.edge_id          in stats.edges_modified
        assert changes.type.from_value == EdgeTypeA
        assert changes.type.to_value   == EdgeTypeB
        assert changes.json()          == { 'from_node': None,
                                            'to_node'  : None,
                                            'type'     : { 'from_value': 'test_MGraph__Diff.EdgeTypeA',
                                                           'to_value'  : 'test_MGraph__Diff.EdgeTypeB'}}


    def test_complex_graph_changes(self):
        class CustomNode(Schema__MGraph__Node): pass                                         # Create custom types
        class CustomEdge(Schema__MGraph__Edge): pass

        with self.graph_a.edit() as edit_a:                                                  # Setup graph A
            node_a1 = edit_a.new_node(node_type = Schema__MGraph__Node)
            node_a2 = edit_a.new_node(node_type = CustomNode          )
            node_a3 = edit_a.new_node(node_type = Schema__MGraph__Node)

            edge_a1 = edit_a.new_edge(from_node_id = node_a1.node_id,
                                      to_node_id   = node_a2.node_id).set_edge_type()
            edge_a2 = edit_a.new_edge(from_node_id = node_a2.node_id,
                                      to_node_id   = node_a3.node_id,
                                      edge_type    = CustomEdge    ).set_edge_type()
        assert node_a1.node_type is  Schema__MGraph__Node


        with self.graph_b.edit() as edit_b:                                                  # Setup graph B with various changes
            node_b1 = edit_b.new_node(node_id = node_a1.node_id, node_type = Schema__MGraph__Node)                             # Keep node_1
            node_b2 = edit_b.new_node(node_id = node_a2.node_id, node_type = Schema__MGraph__Node)                             # Modify node_2
            node_b4 = edit_b.new_node(                           node_type = Schema__MGraph__Node)                                                      # Add node_4 (node_3 removed)

            edge_b1 = edit_b.new_edge(edge_id       = edge_a1.edge_id   ,                     # Modify edge_1
                                      from_node_id = node_b1.node_id   ,
                                      to_node_id   = node_b2.node_id   ,
                                      edge_type    = CustomEdge       ).set_edge_type()
            edge_b3 = edit_b.new_edge(from_node_id = node_b2.node_id,                        # Add edge_3 (edge_2 removed)
                                      to_node_id   = node_b4.node_id).set_edge_type()

        diff  = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats = diff.diff_graphs()

        assert stats.json() == { 'edges_added'     : [edge_b3.edge_id],
                                 'edges_count_diff': 0,
                                 'edges_modified'  : {str(edge_a1.edge_id):  { 'from_node': None,
                                                                               'to_node'  : None,
                                                                               'type'     : { 'from_value': type_full_name(Schema__MGraph__Edge),
                                                                                              'to_value'  : 'test_MGraph__Diff.CustomEdge'      }}},
                                 'edges_removed'   : [edge_a2.edge_id],
                                 'nodes_added'     : [node_b4.node_id],
                                 'nodes_count_diff': 0,
                                 'nodes_modified'  : { str(node_a2.node_id): { 'data': None,
                                                                               'type': { 'from_value': 'test_MGraph__Diff.CustomNode',
                                                                                         'to_value'  : type_full_name(Schema__MGraph__Node)}}},
                                 'nodes_removed'   : [node_a3.node_id] }

    def test_empty_and_null_cases(self):
        diff = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)

        assert diff.compare_node_data(None).obj() == Schema__MGraph__Node__Changes().obj()              # Test comparing non-existent node
        assert diff.compare_edge_data(None).obj() == Schema__MGraph__Edge__Changes().obj()              # Test comparing non-existent edge

        with self.graph_b.edit() as edit_b:                                                             # Compare empty to non-empty graph
            node_b = edit_b.new_node()
            edge_b = edit_b.new_edge(from_node_id = node_b.node_id,
                                    to_node_id   = node_b.node_id)

        stats = diff.diff_graphs()
        assert stats.obj() == __(nodes_added      = [node_b.node_id]    ,
                                nodes_removed     = []                  ,
                                nodes_modified    = __()                ,
                                edges_added       = [edge_b.edge_id]    ,
                                edges_removed     = []                  ,
                                edges_modified    = __()                ,
                                nodes_count_diff  = 1                   ,
                                edges_count_diff  = 1                   )