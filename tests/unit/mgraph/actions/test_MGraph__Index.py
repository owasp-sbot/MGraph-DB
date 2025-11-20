from unittest                                                       import TestCase

from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id   import Safe_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Label           import Schema__MGraph__Edge__Label
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value           import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data     import Schema__MGraph__Node__Value__Data
from mgraph_db.providers.simple.MGraph__Simple__Test_Data           import MGraph__Simple__Test_Data
from osbot_utils.testing.__                                         import __
from osbot_utils.testing.Temp_File                                  import Temp_File
from mgraph_db.mgraph.MGraph                                        import MGraph
from osbot_utils.utils.Files                                        import file_not_exists, file_exists
from mgraph_db.mgraph.actions.MGraph__Index                         import MGraph__Index
from mgraph_db.mgraph.schemas.Schema__MGraph__Index__Data           import Schema__MGraph__Index__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge

class test_MGraph_Index(TestCase):

    def setUp(self):
        self.mgraph_index = MGraph__Index()

    def test__setUp(self):
        with self.mgraph_index as _:
            assert type(_           ) is MGraph__Index
            assert type(_.index_data) is Schema__MGraph__Index__Data
            assert _.json()           == { 'index_data'  : { 'edges_by_incoming_label'        : {},
                                                             'edges_by_outgoing_label'        : {},
                                                             'edges_by_predicate'             : {},
                                                             'edges_by_type'                  : {},
                                                             'edges_predicates'               : {},
                                                             'edges_to_nodes'                 : {},
                                                             'edges_types'                    : {},
                                                             'nodes_by_type'                  : {},
                                                             'nodes_to_incoming_edges_by_type': {},
                                                             'nodes_to_incoming_edges'        : {},
                                                             'nodes_to_outgoing_edges'        : {},
                                                             'nodes_to_outgoing_edges_by_type': {},
                                                             'nodes_types'                    : {}},
                                           'values_index': { 'index_data': { 'hash_to_node'   : {},
                                                                             'node_to_hash'   : {},
                                                                             'type_by_value'  : {},
                                                                             'values_by_type' : {}}}}

    def test_add_node(self):    # Test adding a node to the index
        node_to_add = Schema__MGraph__Node()

        with self.mgraph_index as _:
            _.add_node(node_to_add)

            # Verify node was added to type index
            assert node_to_add.node_type.__name__ in _.index_data.nodes_by_type
            assert node_to_add.node_id in _.index_data.nodes_by_type[node_to_add.node_type.__name__]
            assert node_to_add.node_id in _.index_data.nodes_to_outgoing_edges

    def test_add_edge(self):                                                                                            # Test adding an edge to the index
        node_1  = Schema__MGraph__Node()
        node_2  = Schema__MGraph__Node()
        edge    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        edge_id = edge.edge_id

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge  )

            assert edge.edge_type.__name__ in _.index_data.edges_by_type                                                # Verify edge was added to type and node relationship indexes
            assert edge_id in _.index_data.edges_by_type          [edge.edge_type.__name__]
            assert edge_id in _.index_data.nodes_to_outgoing_edges[node_1.node_id         ]
            assert edge_id in _.index_data.nodes_to_incoming_edges[node_2.node_id         ]

    def test_remove_node(self):                                                                                         # Test removing a node from the index
        node_to_remove = Schema__MGraph__Node()

        with self.mgraph_index as _:
            _.add_node   (node_to_remove)
            _.remove_node(node_to_remove)

            assert node_to_remove.node_type.__name__ not in _.index_data.nodes_by_type                                  # Verify node was removed from type and node indexes
            assert node_to_remove.node_id            not in _.index_data.nodes_to_outgoing_edges
            assert node_to_remove.node_id            not in _.index_data.nodes_to_incoming_edges

    def test_remove_edge(self):                                                                                         # Test removing an edge from the index
        node_1  = Schema__MGraph__Node()
        node_2  = Schema__MGraph__Node()
        edge    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        edge_id = edge.edge_id

        with self.mgraph_index as _:
            _.add_node   (node_1)
            _.add_node   (node_2)
            _.add_edge   (edge  )
            _.remove_edge(edge  )

            assert edge.edge_type.__name__ not in _.index_data.edges_by_type                                            # Verify edge was removed from type and node relationship indexes
            assert edge_id                 not in _.index_data.nodes_to_outgoing_edges.get(node_1.node_id, set())
            assert edge_id                 not in _.index_data.nodes_to_incoming_edges.get(node_2.node_id, set())

    def test_get_methods(self):                                                                                         # Test various get methods of the index
        node_1  = Schema__MGraph__Node()
        node_2  = Schema__MGraph__Node()
        edge    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        edge_id = edge.edge_id

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge  )

            assert node_1.node_id in _.get_nodes_by_type(Schema__MGraph__Node)                                          # Test get methods
            assert edge_id        in _.get_edges_by_type(Schema__MGraph__Edge)

    def test_json(self):
        node_1 = Schema__MGraph__Node()
        node_2 = Schema__MGraph__Node()
        edge_1 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        node_1_id = node_1.node_id
        node_2_id = node_2.node_id
        edge_1_id = edge_1.edge_id

        with self.mgraph_index as _:
            assert _.index_data.obj()  == __(edges_to_nodes                  = __(),
                                             edges_by_type                   = __(),
                                             edges_by_predicate              = __(),
                                             edges_by_incoming_label         = __(),
                                             edges_by_outgoing_label         = __(),
                                             edges_predicates                = __(),
                                             nodes_types                     = __(),
                                             edges_types                     = __(),
                                             nodes_to_outgoing_edges         = __(),
                                             nodes_to_incoming_edges         = __(),
                                             nodes_to_incoming_edges_by_type = __(),
                                             nodes_to_outgoing_edges_by_type = __(),
                                             nodes_by_type                   = __())

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge_1)
            nodes_by_type = _.index_data.nodes_by_type['Schema__MGraph__Node']            # we need to get this value since nodes_by_type is a list and the order can change
            assert node_1_id           in nodes_by_type
            assert node_2_id           in nodes_by_type
            assert _.index_data.json() == { 'edges_by_incoming_label'        : {},
                                            'edges_by_outgoing_label'        : {},
                                            'edges_by_predicate'             : {},
                                            'edges_predicates'               : {},
                                            'edges_to_nodes'                 : { edge_1_id: (node_1_id, node_2_id)},
                                            'edges_by_type'                  : {'Schema__MGraph__Edge': {edge_1_id}},
                                            'edges_types'                    : { edge_1_id: 'Schema__MGraph__Edge'},
                                            'nodes_by_type'                  : {'Schema__MGraph__Node': nodes_by_type },
                                            'nodes_to_incoming_edges'        : { node_2_id: {edge_1_id},
                                                                                 node_1_id: set()},
                                            'nodes_to_incoming_edges_by_type': { node_2_id: {'Schema__MGraph__Edge': {edge_1_id} }},
                                            'nodes_to_outgoing_edges'        : { node_2_id: set(),
                                                                                 node_1_id: {edge_1_id}},
                                            'nodes_to_outgoing_edges_by_type': { node_1_id: {'Schema__MGraph__Edge': {edge_1_id}}},
                                            'nodes_types'                    : { node_1_id: 'Schema__MGraph__Node',
                                                                                 node_2_id: 'Schema__MGraph__Node'}}


    def test__index_data__from_simple_graph(self):
        simple_graph  = MGraph__Simple__Test_Data().create()
        with simple_graph.index() as _:
            assert len(_.edges_to_nodes         ()) == 2
            assert len(_.edges_by_type          ()) == 1
            assert len(_.nodes_by_type          ()) == 1
            assert len(_.nodes_to_incoming_edges()) == 3
            assert len(_.nodes_to_outgoing_edges()) == 3

    def test_from_graph(self):                                                                      # Test creating index from graph using class method
        mgraph    = MGraph()
        node_1    = Schema__MGraph__Node()
        node_2    = Schema__MGraph__Node()
        edge_1    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        node_1_id = node_1.node_id
        node_2_id = node_2.node_id
        edge_1_id = edge_1.edge_id
        edge_1_type = edge_1.edge_type.__name__
        node_1_type = node_1.node_type.__name__

        with mgraph.edit() as _:
            _.add_node(node_1)                                                   # Add nodes and edges to graph
            _.add_node(node_2)
            _.add_edge(edge_1)
        with mgraph.data() as _:
            assert _.nodes_ids() == [node_1_id, node_2_id]
            assert _.edges_ids() == [edge_1_id           ]

        index         = MGraph__Index.from_graph(mgraph.graph)                                                # Create index from graph
        nodes_by_type = index.index_data.nodes_by_type['Schema__MGraph__Node']
        assert node_1_id               in nodes_by_type
        assert node_2_id               in nodes_by_type

        assert index.index_data.json() ==  {  'edges_by_incoming_label'        : {},
                                              'edges_by_outgoing_label'        : {},
                                              'edges_by_predicate'             : {},
                                              'edges_by_type'                  : { edge_1_type: { edge_1_id }        },
                                              'edges_predicates'               : {},
                                              'edges_to_nodes'                 : { edge_1_id: (node_1_id, node_2_id) },

                                              'edges_types'                    : { edge_1_id: 'Schema__MGraph__Edge' },
                                              'nodes_by_type'                  : { node_1_type: nodes_by_type        },
                                              'nodes_to_incoming_edges'        : { node_1_id: set()                   ,
                                                                                   node_2_id: { edge_1_id }          },
                                              'nodes_to_incoming_edges_by_type': { node_2_id: {'Schema__MGraph__Edge': {edge_1_id}}},
                                              'nodes_to_outgoing_edges'        : { node_1_id: {edge_1_id}            ,
                                                                                   node_2_id: set()                  },
                                             'nodes_to_outgoing_edges_by_type' : { node_1_id: {'Schema__MGraph__Edge': {edge_1_id}}},
                                             'nodes_types'                     : { node_1_id: 'Schema__MGraph__Node',
                                                                                   node_2_id: 'Schema__MGraph__Node'}}



    def test_save_to_file__and__from_file(self):                                                             # Test save and load functionality
        node_1 = Schema__MGraph__Node()
        node_2 = Schema__MGraph__Node()
        edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

        with self.mgraph_index as _:
            _.add_node(node_1)                                                                      # Add nodes and edge to index
            _.add_node(node_2)
            _.add_edge(edge)

            with Temp_File(return_file_path=True, extension='json', create_file=False) as target_file:                   # temp file to use

                assert file_not_exists(target_file)
                _.save_to_file(target_file)                                                            # Save to temp file
                assert file_exists(target_file)

                # todo: find a way to make this more deterministic, the use of set() keeps causing everynow and then an CI pipeline error
                # loaded_index = MGraph__Index.from_file(target_file)                                     # Load index from file
                # loaded_index     .index_data.nodes_by_type['Schema__MGraph__Node'] = set(list(loaded_index     .index_data.nodes_by_type['Schema__MGraph__Node']))  # todo: find better way to handle this
                # self.mgraph_index.index_data.nodes_by_type['Schema__MGraph__Node'] = set(list(self.mgraph_index.index_data.nodes_by_type['Schema__MGraph__Node']))  #       we need to do this because the order of this 'set' object can change

                #assert loaded_index.json() == self.mgraph_index.json()                                  # confirm object as the save (original and loaded from disk)
                #assert loaded_index.obj () == self.mgraph_index.obj ()

    def test_get_nodes_connected_to_value(self):
        class Value_Node(Schema__MGraph__Node__Value): pass                                             # Test value node type
        class Test_Edge (Schema__MGraph__Edge       ): pass                                             # Test edge type

        value      = "test_value"
        value_data = Schema__MGraph__Node__Value__Data(value=value, value_type=str)              # Create value node
        value_node = Value_Node(node_data=value_data)

        node_1     = Schema__MGraph__Node()                                                                 # Create connecting nodes
        node_2     = Schema__MGraph__Node()
        node_3     = Schema__MGraph__Node()

        edge_1     = Test_Edge           (from_node_id=node_1.node_id, to_node_id=value_node.node_id)       # Create edges
        edge_2     = Test_Edge           (from_node_id=node_2.node_id, to_node_id=value_node.node_id)
        edge_3     = Schema__MGraph__Edge(from_node_id=node_3.node_id, to_node_id=value_node.node_id)

        print()
        print()
        with self.mgraph_index as _:
            #_.values_index.add_value_node(value_node)
            #_.add_node(value_node)
            _.add_node(value_node)                                                                      # Add all nodes and edges
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)
            _.add_edge(edge_3)

            connected_nodes = _.get_nodes_connected_to_value(value, node_type=Value_Node)                     # Test without edge type filter

            assert len(connected_nodes) == 3
            assert node_1.node_id       in connected_nodes
            assert node_2.node_id       in connected_nodes
            assert node_3.node_id       in connected_nodes

            connected_nodes = _.get_nodes_connected_to_value("test_value", Test_Edge, node_type=Value_Node)          # Test with edge type filter
            assert len(connected_nodes) == 2
            assert node_1.node_id       in connected_nodes
            assert node_2.node_id       in connected_nodes
            assert node_3.node_id       not in connected_nodes

            connected_nodes = _.get_nodes_connected_to_value("non_existent")                   # Test with non-existent value
            assert len(connected_nodes) == 0

    def test_add_edge_with_label(self):                                                     # Test adding an edge with label and verifying index structures

        node_1 = Schema__MGraph__Node()                                                     # Create test nodes and edge
        node_2 = Schema__MGraph__Node()

        edge_label = Schema__MGraph__Edge__Label(predicate    = Safe_Id('created_by'),         # Create an edge with a label
                                                 incoming     = Safe_Id('creator_of'),
                                                 outgoing     = Safe_Id('created'   ))
        edge        = Schema__MGraph__Edge      (from_node_id = node_1.node_id      ,
                                                 to_node_id   = node_2.node_id      ,
                                                 edge_label   = edge_label          )

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge  )

            assert edge.edge_id in _.index_data.edges_by_type[edge.edge_type.__name__]          # Verify regular edge indexing still works


            assert 'created_by' in _.index_data.edges_by_predicate                              # Verify predicate indexing
            assert edge.edge_id in _.index_data.edges_by_predicate['created_by']
            assert _.index_data.edges_predicates[edge.edge_id] == 'created_by'

            assert 'creator_of' in _.index_data.edges_by_incoming_label                         # Verify directional label indexing
            assert edge.edge_id in _.index_data.edges_by_incoming_label['creator_of']

            assert 'created' in _.index_data.edges_by_outgoing_label
            assert edge.edge_id in _.index_data.edges_by_outgoing_label['created']

    def test_remove_edge_with_label(self):                                                      # Test removing an edge with label and ensuring all indexes are cleaned up
        node_1 = Schema__MGraph__Node()                                                         # Create test nodes and edge with label
        node_2 = Schema__MGraph__Node()

        edge_label = Schema__MGraph__Edge__Label(predicate    = Safe_Id('supports'    ),
                                                 incoming     = Safe_Id('supported_by'),
                                                 outgoing     = Safe_Id('supports'    ))
        edge = Schema__MGraph__Edge             (from_node_id = node_1.node_id         ,
                                                 to_node_id   = node_2.node_id         ,
                                                 edge_label   = edge_label             )

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            assert 'supports'     in _.index_data.edges_by_predicate                            # Verify the edge was indexed correctly
            assert 'supported_by' in _.index_data.edges_by_incoming_label

            _.remove_edge(edge)                                                                 # Now remove the edge

            assert 'supports'     not in _.index_data.edges_by_predicate                        # Verify all index entries were cleaned up
            assert 'supported_by' not in _.index_data.edges_by_incoming_label
            assert edge.edge_id   not in _.index_data.edges_predicates

    def test_multiple_edges_with_same_predicate(self):                                          # Test indexing multiple edges with the same predicate

        # Create test nodes
        node_1 = Schema__MGraph__Node()
        node_2 = Schema__MGraph__Node()
        node_3 = Schema__MGraph__Node()

        # Create two edges with the same predicate
        edge_label_1 = Schema__MGraph__Edge__Label(predicate = Safe_Id('references'))
        edge_label_2 = Schema__MGraph__Edge__Label(predicate = Safe_Id('references'))

        edge_1 = Schema__MGraph__Edge(from_node_id = node_1.node_id,
                                     to_node_id   = node_2.node_id,
                                     edge_label   = edge_label_1)

        edge_2 = Schema__MGraph__Edge(from_node_id = node_2.node_id,
                                     to_node_id   = node_3.node_id,
                                     edge_label   = edge_label_2)

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            # Verify both edges are indexed under the same predicate
            assert 'references' in _.index_data.edges_by_predicate
            assert len(_.index_data.edges_by_predicate['references']) == 2
            assert edge_1.edge_id in _.index_data.edges_by_predicate['references']
            assert edge_2.edge_id in _.index_data.edges_by_predicate['references']

            # Remove one edge and verify the other remains indexed
            _.remove_edge(edge_1)
            assert 'references' in _.index_data.edges_by_predicate
            assert len(_.index_data.edges_by_predicate['references']) == 1
            assert edge_2.edge_id in _.index_data.edges_by_predicate['references']

    def test_query_helpers_for_predicates(self):                                    #  Test helper methods for querying edges by predicates
        # Create test data
        node_1 = Schema__MGraph__Node()
        node_2 = Schema__MGraph__Node()
        node_3 = Schema__MGraph__Node()

        edge_label_1 = Schema__MGraph__Edge__Label(predicate = Safe_Id('depends_on'))
        edge_label_2 = Schema__MGraph__Edge__Label(predicate = Safe_Id('depends_on'))
        edge_label_3 = Schema__MGraph__Edge__Label(predicate = Safe_Id('contains'))

        edge_1 = Schema__MGraph__Edge(from_node_id = node_1.node_id,
                                     to_node_id   = node_2.node_id,
                                     edge_label   = edge_label_1)

        edge_2 = Schema__MGraph__Edge(from_node_id = node_1.node_id,
                                     to_node_id   = node_3.node_id,
                                     edge_label   = edge_label_2)

        edge_3 = Schema__MGraph__Edge(from_node_id = node_2.node_id,
                                     to_node_id   = node_3.node_id,
                                     edge_label   = edge_label_3)

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)
            _.add_edge(edge_3)

            # Test get_edges_by_predicate
            depends_on_edges = _.get_edges_by_predicate('depends_on')
            assert len(depends_on_edges) == 2
            assert edge_1.edge_id in depends_on_edges
            assert edge_2.edge_id in depends_on_edges

            contains_edges = _.get_edges_by_predicate('contains')
            assert len(contains_edges) == 1
            assert edge_3.edge_id in contains_edges

            # Test get_node_outgoing_edges_by_predicate
            node1_depends_on_edges = _.get_node_outgoing_edges_by_predicate(node_1.node_id, 'depends_on')
            assert len(node1_depends_on_edges) == 2
            assert edge_1.edge_id in node1_depends_on_edges
            assert edge_2.edge_id in node1_depends_on_edges

            node2_contains_edges = _.get_node_outgoing_edges_by_predicate(node_2.node_id, 'contains')
            assert len(node2_contains_edges) == 1
            assert edge_3.edge_id in node2_contains_edges

            # Test with non-existent predicate
            non_existent_edges = _.get_edges_by_predicate('non_existent')
            assert len(non_existent_edges) == 0