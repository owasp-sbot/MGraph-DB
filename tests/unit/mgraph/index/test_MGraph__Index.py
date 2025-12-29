from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats      import Schema__MGraph__Index__Stats
from mgraph_db.utils.testing.mgraph_test_ids                          import mgraph_test_ids
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id      import Obj_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value             import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data       import Schema__MGraph__Node__Value__Data
from osbot_utils.testing.Temp_File                                    import Temp_File
from osbot_utils.utils.Files                                          import file_not_exists, file_exists
from unittest                                                         import TestCase
from osbot_utils.testing.__                                           import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id     import Safe_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id     import Node_Id
from mgraph_db.mgraph.MGraph                                          import MGraph
from mgraph_db.mgraph.index.MGraph__Index                             import MGraph__Index
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                    import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                    import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Label             import Schema__MGraph__Edge__Label
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data       import Schema__MGraph__Index__Data
from mgraph_db.mgraph.schemas.identifiers.Node_Path                   import Node_Path
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                   import Edge_Path
from mgraph_db.providers.simple.MGraph__Simple__Test_Data             import MGraph__Simple__Test_Data


class test_MGraph_Index(TestCase):

    def setUp(self):
        self.mgraph_index = MGraph__Index()

    def test__setUp(self):
        with self.mgraph_index as _:
            assert type(_           ) is MGraph__Index
            assert type(_.index_data) is Schema__MGraph__Index__Data
            assert _.obj()            == __(index_data   = __SKIP__     ,
                                            index_config = None         ,
                                            edges_index  = __(data         = __SKIP__),
                                            labels_index = __(enabled      = True     ,
                                                              data         = __SKIP__),
                                            paths_index  = __(enabled      = True     ,
                                                              data         = __SKIP__),
                                            edit_index   = __(edges_index  = __SKIP__,
                                                              labels_index = __SKIP__,
                                                              paths_index  = __SKIP__,
                                                              types_index  = __SKIP__,
                                                              values_index = __SKIP__,
                                                              resolver     = __SKIP__ ),
                                            query_index  = __(edges_index  = __SKIP__,
                                                              labels_index = __SKIP__,
                                                              types_index  = __SKIP__,
                                                              values_index = __SKIP__),
                                            stats_index  = __(edges_index  = __SKIP__,
                                                              labels_index = __SKIP__,
                                                              paths_index  = __SKIP__,
                                                              types_index  = __SKIP__),
                                            types_index  = __(enabled      = True                    ,
                                                              data         = __SKIP__),
                                            values_index = __(enabled      = True                    ,
                                                              index_data   = None),
                                            resolver=__(mgraph_defaults=__(node_domain_type='mgraph_db.mgraph.domain.Domain__MGraph__Node.Domain__MGraph__Node',
                                                                           edge_domain_type='mgraph_db.mgraph.domain.Domain__MGraph__Edge.Domain__MGraph__Edge',
                                                                           node_model_type='mgraph_db.mgraph.models.Model__MGraph__Node.Model__MGraph__Node',
                                                                           edge_model_type='mgraph_db.mgraph.models.Model__MGraph__Edge.Model__MGraph__Edge',
                                                                           node_type='mgraph_db.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node',
                                                                           node_data_type='mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data',
                                                                           edge_type='mgraph_db.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge',
                                                                          edge_data_type='mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Data.Schema__MGraph__Edge__Data',
                                                                          graph_type='mgraph_db.mgraph.schemas.Schema__MGraph__Graph.Schema__MGraph__Graph',
                                                                          graph_data_type='mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data.Schema__MGraph__Graph__Data')))


    def test_add_node(self):    # Test adding a node to the index
        node_to_add = Schema__MGraph__Node().set_node_type()
        with self.mgraph_index as _:
            _.add_node(node_to_add)

            # Verify node was added to type index
            assert node_to_add.node_type.__name__ in _.index_data.types.nodes_by_type
            assert node_to_add.node_id in _.index_data.types.nodes_by_type[node_to_add.node_type.__name__]
            assert node_to_add.node_id in _.index_data.edges.nodes_to_outgoing_edges

    def test_add_edge(self):                                                                                            # Test adding an edge to the index
        node_1  = Schema__MGraph__Node().set_node_type()
        node_2  = Schema__MGraph__Node().set_node_type()
        edge    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        edge_id = edge.edge_id

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge  )

            assert edge.__class__.__name__ in _.index_data.types.edges_by_type                                                # Verify edge was added to type and node relationship indexes
            assert edge_id in _.index_data.types.edges_by_type          [edge.__class__.__name__]
            assert edge_id in _.index_data.edges.nodes_to_outgoing_edges[node_1.node_id         ]
            assert edge_id in _.index_data.edges.nodes_to_incoming_edges[node_2.node_id         ]

    def test_remove_node(self):                                                                                         # Test removing a node from the index
        node_to_remove = Schema__MGraph__Node(node_type=Schema__MGraph__Node)

        with self.mgraph_index as _:
            _.add_node   (node_to_remove)
            _.remove_node(node_to_remove)

            assert node_to_remove.node_type.__name__ not in _.index_data.types.nodes_by_type                                  # Verify node was removed from type and node indexes
            assert node_to_remove.node_id            not in _.index_data.edges.nodes_to_outgoing_edges
            assert node_to_remove.node_id            not in _.index_data.edges.nodes_to_incoming_edges

    def test_remove_edge(self):                                                                                         # Test removing an edge from the index
        node_1  = Schema__MGraph__Node().set_node_type()
        node_2  = Schema__MGraph__Node().set_node_type()
        edge    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id).set_edge_type()
        edge_id = edge.edge_id

        with self.mgraph_index as _:
            _.add_node   (node_1)
            _.add_node   (node_2)
            _.add_edge   (edge  )
            _.remove_edge(edge  )

            assert edge.edge_type.__name__ not in _.index_data.types.edges_by_type                                            # Verify edge was removed from type and node relationship indexes
            assert edge_id                 not in _.index_data.edges.nodes_to_outgoing_edges.get(node_1.node_id, set())
            assert edge_id                 not in _.index_data.edges.nodes_to_incoming_edges.get(node_2.node_id, set())

    def test_get_methods(self):                                                                                         # Test various get methods of the index
        node_1  = Schema__MGraph__Node().set_node_type()
        node_2  = Schema__MGraph__Node().set_node_type()
        edge    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        edge_id = edge.edge_id

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge  )

            assert node_1.node_id in _.get_nodes_by_type(Schema__MGraph__Node)                                          # Test get methods
            assert edge_id        in _.get_edges_by_type(Schema__MGraph__Edge)

    def test_json(self):
        node_1 = Schema__MGraph__Node().set_node_type()
        node_2 = Schema__MGraph__Node().set_node_type()
        edge_1 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        node_1_id = node_1.node_id
        node_2_id = node_2.node_id
        edge_1_id = edge_1.edge_id

        # Convert to primitive strings for JSON comparison
        node_1_id_str = str(node_1_id)
        node_2_id_str = str(node_2_id)
        edge_1_id_str = str(edge_1_id)

        with self.mgraph_index as _:
            assert _.index_data.obj()  == __(edges  = __(edges_to_nodes         = __(),
                                                         nodes_to_outgoing_edges = __(),
                                                         nodes_to_incoming_edges = __()),
                                             labels = __(edges_predicates        = __(),
                                                         edges_by_predicate      = __(),
                                                         edges_incoming_labels   = __(),
                                                         edges_by_incoming_label = __(),
                                                         edges_outgoing_labels   = __(),
                                                         edges_by_outgoing_label = __()),
                                             paths  = __(nodes_by_path           = __(),
                                                         edges_by_path           = __()),
                                             types  = __(nodes_types                     = __(),
                                                         nodes_by_type                   = __(),
                                                         edges_types                     = __(),
                                                         edges_by_type                   = __(),
                                                         nodes_to_incoming_edges_by_type = __(),
                                                         nodes_to_outgoing_edges_by_type = __()))

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge_1)
            nodes_by_type = _.index_data.types.nodes_by_type['Schema__MGraph__Node']            # we need to get this value since nodes_by_type is a list and the order can change
            assert node_1_id           in nodes_by_type
            assert node_2_id           in nodes_by_type

            # Convert nodes_by_type to primitive strings for comparison
            nodes_by_type_json = sorted([ str(n) for n in nodes_by_type ])

            index_data_json = _.index_data.json()
            index_data_json.get('types').get('nodes_by_type').get('Schema__MGraph__Node').sort()
            assert index_data_json     == { 'edges' : { 'edges_to_nodes'          : { edge_1_id_str: [node_1_id_str, node_2_id_str]} ,
                                                        'nodes_to_outgoing_edges' : { node_1_id_str: [edge_1_id_str]                 ,
                                                                                      node_2_id_str: []}                             ,
                                                        'nodes_to_incoming_edges' : { node_1_id_str: []                              ,
                                                                                      node_2_id_str: [edge_1_id_str]}                },
                                            'labels': { 'edges_predicates'        : {}                                               ,
                                                        'edges_by_predicate'      : {}                                               ,
                                                        'edges_incoming_labels'   : {}                                               ,
                                                        'edges_by_incoming_label' : {}                                               ,
                                                        'edges_outgoing_labels'   : {}                                               ,
                                                        'edges_by_outgoing_label' : {}                                               },
                                            'paths' : { 'nodes_by_path'           : {}                                               ,
                                                        'edges_by_path'           : {}                                               },
                                            'types' : { 'nodes_types'             : { node_1_id_str: 'Schema__MGraph__Node'          ,
                                                                                      node_2_id_str: 'Schema__MGraph__Node'}         ,
                                                        'nodes_by_type'           : {'Schema__MGraph__Node': nodes_by_type_json }    ,
                                                        'edges_types'             : { edge_1_id_str: 'Schema__MGraph__Edge'}         ,
                                                        'edges_by_type'           : {'Schema__MGraph__Edge': [edge_1_id_str]}        ,
                                                        'nodes_to_incoming_edges_by_type': { node_2_id_str: {'Schema__MGraph__Edge': [edge_1_id_str] }},
                                                        'nodes_to_outgoing_edges_by_type': { node_1_id_str: {'Schema__MGraph__Edge': [edge_1_id_str]}}}}

    def test__index_data__from_simple_graph(self):
        simple_graph  = MGraph__Simple__Test_Data().create()
        with simple_graph.index() as _:
            assert len(_.edges_to_nodes         ()) == 2
            assert len(_.edges_by_type          ()) == 1
            assert len(_.nodes_by_type          ()) == 1
            assert len(_.nodes_to_incoming_edges()) == 3
            assert len(_.nodes_to_outgoing_edges()) == 3

    def test_from_graph(self):                                                                      # Test creating index from graph using class method
        with mgraph_test_ids():
            mgraph    = MGraph()
            node_1    = Schema__MGraph__Node().set_node_type()
            node_2    = Schema__MGraph__Node().set_node_type()
            edge_1    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id).set_edge_type()
            node_1_id = node_1.node_id
            node_2_id = node_2.node_id
            edge_1_id = edge_1.edge_id
            edge_1_type = edge_1.edge_type.__name__
            node_1_type = node_1.node_type.__name__

            # Convert to primitive strings for JSON comparison
            node_1_id_str = str(node_1_id)
            node_2_id_str = str(node_2_id)
            edge_1_id_str = str(edge_1_id)

            with mgraph.edit() as _:
                _.add_node(node_1)                                                   # Add nodes and edges to graph
                _.add_node(node_2)
                _.add_edge(edge_1)
            with mgraph.data() as _:
                assert _.nodes_ids() == [node_1_id, node_2_id]
                assert _.edges_ids() == [edge_1_id           ]

            index         = MGraph__Index.from_graph(mgraph.graph.model.data)                                                # Create index from graph
            nodes_by_type = index.index_data.types.nodes_by_type['Schema__MGraph__Node']
            assert node_1_id               in nodes_by_type
            assert node_2_id               in nodes_by_type

            # Convert nodes_by_type to primitive strings for comparison
            nodes_by_type_json = ['c0000001', 'c0000002']                   # they are deterministic due to use of mgraph_test_ids

            assert index.index_data.json() ==  {  'edges' : { 'edges_to_nodes'          : { edge_1_id_str: [node_1_id_str, node_2_id_str]},
                                                              'nodes_to_outgoing_edges' : { node_1_id_str: [edge_1_id_str]               ,
                                                                                            node_2_id_str: []                         },
                                                              'nodes_to_incoming_edges' : { node_1_id_str: []                         ,
                                                                                            node_2_id_str: [ edge_1_id_str ]             }},
                                                  'labels': { 'edges_predicates'        : {}                                              ,
                                                              'edges_by_predicate'      : {}                                              ,
                                                              'edges_incoming_labels'   : {}                                              ,
                                                              'edges_by_incoming_label' : {}                                              ,
                                                              'edges_outgoing_labels'   : {}                                              ,
                                                              'edges_by_outgoing_label' : {}                                              },
                                                  'paths' : { 'nodes_by_path'           : {}                                              ,
                                                              'edges_by_path'           : {}                                              },
                                                  'types' : { 'nodes_types'             : { node_1_id_str: 'Schema__MGraph__Node'        ,
                                                                                            node_2_id_str: 'Schema__MGraph__Node'        },
                                                              'nodes_by_type'           : { node_1_type: nodes_by_type_json              },
                                                              'edges_types'             : { edge_1_id_str: 'Schema__MGraph__Edge'        },
                                                              'edges_by_type'           : { edge_1_type: [ edge_1_id_str ]               },
                                                              'nodes_to_incoming_edges_by_type': { node_2_id_str: {'Schema__MGraph__Edge': [edge_1_id_str]}},
                                                              'nodes_to_outgoing_edges_by_type': { node_1_id_str: {'Schema__MGraph__Edge': [edge_1_id_str]}}}}

    def test_from_graph__with_pre_defined_node_ids(self):                                                                      # Test creating index from graph using class method
        node_1_id = 'aaaaaaaa'
        node_2_id = 'bbbbbbbb'
        edge_1_id = 'cccccccc'
        mgraph    = MGraph()
        node_1    = Schema__MGraph__Node(node_id=node_1_id).set_node_type()
        node_2    = Schema__MGraph__Node(node_id=node_2_id).set_node_type()
        edge_1    = Schema__MGraph__Edge(edge_id=edge_1_id, from_node_id=node_1.node_id, to_node_id=node_2.node_id).set_edge_type()

        with mgraph.edit() as _:
            _.add_node(node_1)                                                   # Add nodes and edges to graph
            _.add_node(node_2)
            _.add_edge(edge_1)

        with mgraph.data() as _:
            assert _.nodes_ids() == [node_1_id, node_2_id]
            assert _.edges_ids() == [edge_1_id           ]

        index         = MGraph__Index.from_graph(mgraph.graph.model.data)                                                # Create index from graph
        nodes_by_type = sorted(index.index_data.types.nodes_by_type['Schema__MGraph__Node'])

        assert nodes_by_type          == [node_1_id, node_2_id]
        assert index.index_data.obj() == __(edges  = __(edges_to_nodes         = __(cccccccc = __SKIP__),
                                                        nodes_to_outgoing_edges = __(aaaaaaaa = ['cccccccc'],
                                                                                     bbbbbbbb = []),
                                                        nodes_to_incoming_edges = __(aaaaaaaa = [],
                                                                                     bbbbbbbb = ['cccccccc'])),
                                            labels = __(edges_predicates        = __(),
                                                        edges_by_predicate      = __(),
                                                        edges_incoming_labels   = __(),
                                                        edges_by_incoming_label = __(),
                                                        edges_outgoing_labels   = __(),
                                                        edges_by_outgoing_label = __()),
                                            paths  = __(nodes_by_path           = __(),
                                                        edges_by_path           = __()),
                                            types  = __(nodes_types                     = __(aaaaaaaa = 'Schema__MGraph__Node',
                                                                                             bbbbbbbb = 'Schema__MGraph__Node'),
                                                        nodes_by_type                   = __(Schema__MGraph__Node = __SKIP__),
                                                        edges_types                     = __(cccccccc = 'Schema__MGraph__Edge'),
                                                        edges_by_type                   = __(Schema__MGraph__Edge = ['cccccccc']),
                                                        nodes_to_incoming_edges_by_type = __(bbbbbbbb = __(Schema__MGraph__Edge = ['cccccccc'])),
                                                        nodes_to_outgoing_edges_by_type = __(aaaaaaaa = __(Schema__MGraph__Edge = ['cccccccc']))))


    def test_save_to_file__and__from_file(self):                                                             # Test save and load functionality
        node_1 = Schema__MGraph__Node().set_node_type()
        node_2 = Schema__MGraph__Node().set_node_type()
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
                # loaded_index     .index_data.types.nodes_by_type['Schema__MGraph__Node'] = set(list(loaded_index     .index_data.types.nodes_by_type['Schema__MGraph__Node']))  # todo: find better way to handle this
                # self.mgraph_index.index_data.types.nodes_by_type['Schema__MGraph__Node'] = set(list(self.mgraph_index.index_data.types.nodes_by_type['Schema__MGraph__Node']))  #       we need to do this because the order of this 'set' object can change

                #assert loaded_index.json() == self.mgraph_index.json()                                  # confirm object as the save (original and loaded from disk)
                #assert loaded_index.obj () == self.mgraph_index.obj ()

    def test_get_nodes_connected_to_value(self):
        class Value_Node(Schema__MGraph__Node__Value): pass                                             # Test value node type
        class Test_Edge (Schema__MGraph__Edge       ): pass                                             # Test edge type

        value      = "test_value"
        value_data = Schema__MGraph__Node__Value__Data(value=value, value_type=str)              # Create value node
        value_node = Value_Node(node_data=value_data).set_node_type()

        node_1     = Schema__MGraph__Node().set_node_type()                                                 # Create connecting nodes
        node_2     = Schema__MGraph__Node().set_node_type()
        node_3     = Schema__MGraph__Node().set_node_type()

        edge_1     = Test_Edge           (from_node_id=node_1.node_id, to_node_id=value_node.node_id).set_edge_type()       # Create edges
        edge_2     = Test_Edge           (from_node_id=node_2.node_id, to_node_id=value_node.node_id).set_edge_type()
        edge_3     = Schema__MGraph__Edge(from_node_id=node_3.node_id, to_node_id=value_node.node_id).set_edge_type()

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

        node_1 = Schema__MGraph__Node().set_node_type()                                     # Create test nodes and edge
        node_2 = Schema__MGraph__Node().set_node_type()

        edge_label = Schema__MGraph__Edge__Label(predicate    = Safe_Id('created_by'),         # Create an edge with a label
                                                 incoming     = Safe_Id('creator_of'),
                                                 outgoing     = Safe_Id('created'   ))
        edge        = Schema__MGraph__Edge      (from_node_id = node_1.node_id      ,
                                                 to_node_id   = node_2.node_id      ,
                                                 edge_label   = edge_label          ).set_edge_type()

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge  )

            assert edge.edge_id in _.index_data.types.edges_by_type[edge.edge_type.__name__]          # Verify regular edge indexing still works


            assert 'created_by' in _.index_data.labels.edges_by_predicate                              # Verify predicate indexing
            assert edge.edge_id in _.index_data.labels.edges_by_predicate['created_by']
            assert _.index_data.labels.edges_predicates[edge.edge_id] == 'created_by'

            assert 'creator_of' in _.index_data.labels.edges_by_incoming_label                         # Verify directional label indexing
            assert edge.edge_id in _.index_data.labels.edges_by_incoming_label['creator_of']

            assert 'created' in _.index_data.labels.edges_by_outgoing_label
            assert edge.edge_id in _.index_data.labels.edges_by_outgoing_label['created']

    def test_remove_edge_with_label(self):                                                      # Test removing an edge with label and ensuring all indexes are cleaned up
        with mgraph_test_ids():
            node_1 = Schema__MGraph__Node().set_node_type()                                         # Create test nodes and edge with label
            node_2 = Schema__MGraph__Node().set_node_type()

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

                assert _.index_data.obj() == __(edges  = __(edges_to_nodes         = __(e0000001=['c0000001', 'c0000002']),
                                                                nodes_to_outgoing_edges = __(c0000001=['e0000001'], c0000002=[]),
                                                                nodes_to_incoming_edges = __(c0000001=[], c0000002=['e0000001'])),
                                                labels = __(edges_predicates        = __(e0000001='supports'),
                                                                edges_by_predicate      = __(supports=['e0000001']),
                                                                edges_incoming_labels   = __(e0000001='supported_by'),
                                                                edges_by_incoming_label = __(supported_by=['e0000001']),
                                                                edges_outgoing_labels   = __(e0000001='supports'),
                                                                edges_by_outgoing_label = __(supports=['e0000001'])),
                                                paths  = __(nodes_by_path           = __(),
                                                                edges_by_path           = __()),
                                                types  = __(nodes_types                     = __(c0000001='Schema__MGraph__Node',
                                                                                                 c0000002='Schema__MGraph__Node'),
                                                                nodes_by_type                   = __(Schema__MGraph__Node=['c0000001', 'c0000002']),
                                                                edges_types                     = __(e0000001='Schema__MGraph__Edge'),
                                                                edges_by_type                   = __(Schema__MGraph__Edge=['e0000001']),
                                                                nodes_to_incoming_edges_by_type = __(c0000002=__(Schema__MGraph__Edge=['e0000001'])),
                                                                nodes_to_outgoing_edges_by_type = __(c0000001=__(Schema__MGraph__Edge=['e0000001'])))) != __()


                assert 'supports'     in _.index_data.labels.edges_by_predicate                            # Verify the edge was indexed correctly
                assert 'supported_by' in _.index_data.labels.edges_by_incoming_label

                assert edge.obj() == __(edge_data=None,
                                        edge_type=None,
                                        edge_label=__(incoming='supported_by',
                                                      outgoing='supports',
                                                      predicate='supports'),
                                        edge_path=None,
                                        from_node_id='c0000001',
                                        to_node_id='c0000002',
                                        edge_id='e0000001')
                _.remove_edge(edge)                                                                 # Now remove the edge

                assert _.index_data.obj() == __(edges  = __(edges_to_nodes         = __(),
                                                                nodes_to_outgoing_edges = __(c0000001=[], c0000002=[]),
                                                                nodes_to_incoming_edges = __(c0000001=[], c0000002=[])),
                                                labels = __(edges_predicates        = __(),
                                                                edges_by_predicate      = __(),
                                                                edges_incoming_labels   = __(),
                                                                edges_by_incoming_label = __(),
                                                                edges_outgoing_labels   = __(),
                                                                edges_by_outgoing_label = __()),
                                                paths  = __(nodes_by_path           = __(),
                                                                edges_by_path           = __()),
                                                types  = __(nodes_types                     = __(c0000001='Schema__MGraph__Node',
                                                                                                 c0000002='Schema__MGraph__Node'),
                                                                nodes_by_type                   = __(Schema__MGraph__Node=['c0000001', 'c0000002']),
                                                                edges_types                     = __(),
                                                                edges_by_type                   = __(),
                                                                nodes_to_incoming_edges_by_type = __(),
                                                                nodes_to_outgoing_edges_by_type = __())) != __()


                assert 'supports'     not in _.index_data.labels.edges_by_predicate                    # Verify all index entries were cleaned up
                assert 'supported_by' not in _.index_data.labels.edges_by_incoming_label               # (before this was passing)
                assert edge.edge_id   not in _.index_data.labels.edges_predicates

    def test_multiple_edges_with_same_predicate(self):                                          # Test indexing multiple edges with the same predicate

        # Create test nodes
        node_1 = Schema__MGraph__Node().set_node_type()
        node_2 = Schema__MGraph__Node().set_node_type()
        node_3 = Schema__MGraph__Node().set_node_type()

        # Create two edges with the same predicate
        edge_label_1 = Schema__MGraph__Edge__Label(predicate = Safe_Id('references'))
        edge_label_2 = Schema__MGraph__Edge__Label(predicate = Safe_Id('references'))

        edge_1 = Schema__MGraph__Edge(from_node_id = node_1.node_id,
                                      to_node_id   = node_2.node_id,
                                      edge_label   = edge_label_1 ).set_edge_type()

        edge_2 = Schema__MGraph__Edge(from_node_id = node_2.node_id,
                                      to_node_id   = node_3.node_id,
                                      edge_label   = edge_label_2 ).set_edge_type()

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            # Verify both edges are indexed under the same predicate
            assert 'references' in _.index_data.labels.edges_by_predicate
            assert len(_.index_data.labels.edges_by_predicate['references']) == 2
            assert edge_1.edge_id in _.index_data.labels.edges_by_predicate['references']
            assert edge_2.edge_id in _.index_data.labels.edges_by_predicate['references']

            # Remove one edge and verify the other remains indexed
            _.remove_edge(edge_1)
            assert 'references' in _.index_data.labels.edges_by_predicate
            assert len(_.index_data.labels.edges_by_predicate['references']) == 1
            assert edge_2.edge_id in _.index_data.labels.edges_by_predicate['references']

    def test_query_helpers_for_predicates(self):                                    #  Test helper methods for querying edges by predicates
        # Create test data
        node_1 = Schema__MGraph__Node().set_node_type()
        node_2 = Schema__MGraph__Node().set_node_type()
        node_3 = Schema__MGraph__Node().set_node_type()

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


    # test_MGraph__Index__Path_Query_Methods(TestCase):

    def test_get_all_node_paths__empty_index(self):                              # Test with no paths
        with self.mgraph_index as _:
            result = _.get_all_node_paths()

            assert type(result) is set
            assert len(result)  == 0

    def test_get_all_node_paths__with_paths(self):                               # Test with nodes having paths
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node(node_path=Node_Path("root.child1"))
            node_2 = Schema__MGraph__Node(node_path=Node_Path("root.child2"))
            node_3 = Schema__MGraph__Node(node_path=Node_Path("root.child1"))    # Same path as node_1

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)

            result = _.get_all_node_paths()

            assert type(result)                      is set
            assert len(result)                       == 2                        # Two unique paths
            assert Node_Path("root.child1")          in result
            assert Node_Path("root.child2")          in result

    def test_get_all_edge_paths__empty_index(self):                              # Test with no edge paths
        with self.mgraph_index as _:
            result = _.get_all_edge_paths()

            assert type(result) is set
            assert len(result)  == 0

    def test_get_all_edge_paths__with_paths(self):                               # Test with edges having paths
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            node_3 = Schema__MGraph__Node().set_node_type()

            edge_1 = Schema__MGraph__Edge(from_node_id = node_1.node_id           ,
                                          to_node_id   = node_2.node_id           ,
                                          edge_path    = Edge_Path("conn.type_a") )
            edge_2 = Schema__MGraph__Edge(from_node_id = node_2.node_id           ,
                                          to_node_id   = node_3.node_id           ,
                                          edge_path    = Edge_Path("conn.type_b") )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            result = _.get_all_edge_paths()

            assert len(result)                      == 2
            assert Edge_Path("conn.type_a")         in result
            assert Edge_Path("conn.type_b")         in result

    def test_get_node_path__found(self):                                         # Test finding a node's path
        with self.mgraph_index as _:
            node = Schema__MGraph__Node(node_path=Node_Path("test.path"))
            _.add_node(node)

            result = _.get_node_path(node.node_id)

            assert result == Node_Path("test.path")

    def test_get_node_path__not_found(self):                                     # Test node without path
        with self.mgraph_index as _:
            node = Schema__MGraph__Node().set_node_type()                        # No path
            _.add_node(node)

            result = _.get_node_path(node.node_id)

            assert result is None

    def test_get_node_path__nonexistent_node(self):                              # Test with nonexistent node_id
        with self.mgraph_index as _:
            result = _.get_node_path(Node_Id(Obj_Id()))

            assert result is None

    def test_get_edge_path__found(self):                                         # Test finding an edge's path
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id = node_1.node_id          ,
                                          to_node_id   = node_2.node_id          ,
                                          edge_path    = Edge_Path("edge.path")  )
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.get_edge_path(edge.edge_id)

            assert result == Edge_Path("edge.path")

    def test_get_edge_path__not_found(self):                                     # Test edge without path
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.get_edge_path(edge.edge_id)

            assert result is None

    def test_count_nodes_by_path__multiple(self):                                # Test counting nodes at path
        with self.mgraph_index as _:
            path = Node_Path("shared.path")
            node_1 = Schema__MGraph__Node(node_path=path)
            node_2 = Schema__MGraph__Node(node_path=path)
            node_3 = Schema__MGraph__Node(node_path=path)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)

            assert _.count_nodes_by_path(path) == 3

    def test_count_nodes_by_path__nonexistent(self):                             # Test counting at nonexistent path
        with self.mgraph_index as _:
            assert _.count_nodes_by_path(Node_Path("nonexistent")) == 0

    def test_count_edges_by_path__multiple(self):                                # Test counting edges at path
        with self.mgraph_index as _:
            path   = Edge_Path("shared.edge.path")
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            node_3 = Schema__MGraph__Node().set_node_type()

            edge_1 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id, edge_path=path)
            edge_2 = Schema__MGraph__Edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id, edge_path=path)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            assert _.count_edges_by_path(path) == 2

    def test_has_node_path__exists(self):                                        # Test path existence check
        with self.mgraph_index as _:
            path = Node_Path("existing.path")
            node = Schema__MGraph__Node(node_path=path)
            _.add_node(node)

            assert _.has_node_path(path)               is True
            assert _.has_node_path(Node_Path("other")) is False

    def test_has_edge_path__exists(self):                                        # Test edge path existence check
        with self.mgraph_index as _:
            path   = Edge_Path("existing.edge")
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id, edge_path=path)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            assert _.has_edge_path(path)               is True
            assert _.has_edge_path(Edge_Path("other")) is False


    # =============================================================================
    # Predicate Methods Tests
    # =============================================================================


    def test_get_nodes_by_predicate__found(self):                                # Test getting target nodes via predicate
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            node_3 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(predicate=Safe_Id('has_child'))
            edge_1     = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     )
            edge_2     = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_3.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            result = _.get_nodes_by_predicate(node_1.node_id, Safe_Id('has_child'))

            assert len(result)     == 2
            assert node_2.node_id  in result
            assert node_3.node_id  in result

    def test_get_nodes_by_predicate__not_found(self):                            # Test with no matching predicate
        with self.mgraph_index as _:
            node = Schema__MGraph__Node().set_node_type()
            _.add_node(node)

            result = _.get_nodes_by_predicate(node.node_id, Safe_Id('nonexistent'))

            assert len(result) == 0

    def test_get_node_incoming_edges_by_predicate(self):                         # Test incoming edges by predicate
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            node_3 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(predicate=Safe_Id('parent_of'))
            edge_1     = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_3.node_id ,
                                              edge_label   = edge_label     )
            edge_2     = Schema__MGraph__Edge(from_node_id = node_2.node_id ,
                                              to_node_id   = node_3.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            result = _.get_node_incoming_edges_by_predicate(node_3.node_id, Safe_Id('parent_of'))

            assert len(result)    == 2
            assert edge_1.edge_id in result
            assert edge_2.edge_id in result

    def test_get_edges_by_incoming_label(self):                                  # Test edges by incoming label
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(incoming=Safe_Id('receiver'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.get_edges_by_incoming_label(Safe_Id('receiver'))

            assert len(result)   == 1
            assert edge.edge_id  in result

    def test_get_edges_by_outgoing_label(self):                                  # Test edges by outgoing label
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(outgoing=Safe_Id('sender'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.get_edges_by_outgoing_label(Safe_Id('sender'))

            assert len(result)   == 1
            assert edge.edge_id  in result


    # =============================================================================
    #  Raw Accessor Methods Tests
    # =============================================================================

    def test_edges_predicates__accessor(self):                                   # Test raw edges_predicates accessor
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(predicate=Safe_Id('test_pred'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.edges_predicates()

            assert type(result)                   is Type_Safe__Dict
            assert result[edge.edge_id]           == Safe_Id('test_pred')

    def test_edges_by_predicate_all__accessor(self):                             # Test raw edges_by_predicate accessor
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(predicate=Safe_Id('my_pred'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.edges_by_predicate_all()

            assert type(result)                       is Type_Safe__Dict
            assert Safe_Id('my_pred')                 in result
            assert edge.edge_id                       in result[Safe_Id('my_pred')]

    def test_edges_by_incoming_label__accessor(self):                            # Test raw incoming label accessor
        with self.mgraph_index as _:
            result = _.edges_by_incoming_label()

            assert type(result) is Type_Safe__Dict
            assert result       == {}

    def test_edges_by_outgoing_label__accessor(self):                            # Test raw outgoing label accessor
        with self.mgraph_index as _:
            result = _.edges_by_outgoing_label()

            assert type(result) is Type_Safe__Dict
            assert result       == {}

    def test_nodes_by_path__accessor(self):                                      # Test raw nodes_by_path accessor
        with self.mgraph_index as _:
            path = Node_Path("test.path")
            node = Schema__MGraph__Node(node_path=path)
            _.add_node(node)

            result = _.nodes_by_path()

            assert type(result)         is Type_Safe__Dict
            assert path                 in result
            assert node.node_id         in result[path]

    def test_edges_by_path__accessor(self):                                      # Test raw edges_by_path accessor
        with self.mgraph_index as _:
            path   = Edge_Path("test.edge.path")
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id, edge_path=path)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.edges_by_path()

            assert type(result)         is Type_Safe__Dict
            assert path                 in result
            assert edge.edge_id         in result[path]


    # =============================================================================
    # Enhanced Stats Tests
    # =============================================================================


    def test_stats__empty_index(self):                                           # Test stats with empty index
        with self.mgraph_index as _:
            stats = _.stats()

            assert _.stats().obj() == __(index_data=__(edge_to_nodes=0,
                                                       edges_by_type=__(),
                                                       edges_by_path=__(),
                                                       nodes_by_type=__(),
                                                       nodes_by_path=__(),
                                                       node_edge_connections=__(total_nodes=0,
                                                                                avg_incoming_edges=0,
                                                                                avg_outgoing_edges=0,
                                                                                max_incoming_edges=0,
                                                                                max_outgoing_edges=0)),
                                         summary=__(total_nodes=0,
                                                    total_edges=0,
                                                    total_predicates=0,
                                                    unique_node_paths=0,
                                                    unique_edge_paths=0,
                                                    nodes_with_paths=0,
                                                    edges_with_paths=0),
                                         paths=__(node_paths=__(),
                                                  edge_paths=__()))
    def test_stats__with_data(self):                                             # Test stats with data
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node(node_path=Node_Path("path.a"))
            node_2 = Schema__MGraph__Node(node_path=Node_Path("path.b"))
            node_3 = Schema__MGraph__Node(node_path=Node_Path("path.a"))         # Same path as node_1

            edge_label = Schema__MGraph__Edge__Label(predicate=Safe_Id('connects'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id           ,
                                              to_node_id   = node_2.node_id           ,
                                              edge_label   = edge_label               ,
                                              edge_path    = Edge_Path("edge.path")   )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge)

            assert _.stats().obj() == __(index_data=__(edge_to_nodes=1,
                                                       edges_by_type=__(Schema__MGraph__Edge=1),
                                                       edges_by_path=__(edge_path=1),
                                                       nodes_by_type=__(Schema__MGraph__Node=3),
                                                       nodes_by_path=__(path_a=2, path_b=1),
                                                       node_edge_connections=__(total_nodes=3,
                                                                                avg_incoming_edges=0,
                                                                                avg_outgoing_edges=0,
                                                                                max_incoming_edges=1,
                                                                                max_outgoing_edges=1)),
                                         summary=__(total_nodes=3,
                                                    total_edges=1,
                                                    total_predicates=1,
                                                    unique_node_paths=2,                # path.a and path.b
                                                    unique_edge_paths=1,
                                                    nodes_with_paths=3,
                                                    edges_with_paths=1),
                                         paths=__(node_paths=__(path_a=2, path_b=1),
                                                  edge_paths=__(edge_path=1)))

    def test_stats__paths_section(self):                                         # Test paths section in stats
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node(node_path=Node_Path("root"))
            node_2 = Schema__MGraph__Node(node_path=Node_Path("root"))
            node_3 = Schema__MGraph__Node(node_path=Node_Path("leaf"))

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)

            assert _.stats().obj() == __(index_data=__(edge_to_nodes=0,
                                                       edges_by_type=__(),
                                                       edges_by_path=__(),
                                                       nodes_by_type=__(Schema__MGraph__Node=3),
                                                       nodes_by_path=__(root=2, leaf=1),
                                                       node_edge_connections=__(total_nodes=3,
                                                                                avg_incoming_edges=0,
                                                                                avg_outgoing_edges=0,
                                                                                max_incoming_edges=0,
                                                                                max_outgoing_edges=0)),
                                         summary=__(total_nodes=3,
                                                    total_edges=0,
                                                    total_predicates=0,
                                                    unique_node_paths=2,
                                                    unique_edge_paths=0,
                                                    nodes_with_paths=3,
                                                    edges_with_paths=0),
                                         paths=__(node_paths=__(root=2, leaf=1),
                                                  edge_paths=__()))


            stats = _.stats()

    def test_stats__index_data_preserved(self):                                  # Test that index_data section preserved
        with self.mgraph_index as _:
            node = Schema__MGraph__Node().set_node_type()
            _.add_node(node)

            stats = _.stats()
            assert type(stats) is Schema__MGraph__Index__Stats
            assert stats.obj() == __(index_data=__(edge_to_nodes=0,
                                                   edges_by_type=__(),
                                                   edges_by_path=__(),
                                                   nodes_by_type=__(Schema__MGraph__Node=1),
                                                   nodes_by_path=__(),
                                                   node_edge_connections=__(total_nodes=1,
                                                                            avg_incoming_edges=0,
                                                                            avg_outgoing_edges=0,
                                                                            max_incoming_edges=0,
                                                                            max_outgoing_edges=0)),
                                    summary=__(total_nodes=1,
                                               total_edges=0,
                                               total_predicates=0,
                                               unique_node_paths=0,
                                               unique_edge_paths=0,
                                               nodes_with_paths=0,
                                               edges_with_paths=0),
                                    paths=__(node_paths=__(), edge_paths=__()))


    # =============================================================================
    # Additional Method Coverage
    # =============================================================================


    def test_edges_ids__from__node_id(self):                                     # Test outgoing edge IDs
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            node_3 = Schema__MGraph__Node().set_node_type()

            edge_1 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_3.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            result = _.edges_ids__from__node_id(node_1.node_id)

            assert type(result)   is list
            assert len(result)    == 2
            assert edge_1.edge_id in result
            assert edge_2.edge_id in result

    def test_edges_ids__to__node_id(self):                                       # Test incoming edge IDs
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            node_3 = Schema__MGraph__Node().set_node_type()

            edge_1 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_3.node_id)
            edge_2 = Schema__MGraph__Edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            result = _.edges_ids__to__node_id(node_3.node_id)

            assert type(result)   is list
            assert len(result)    == 2
            assert edge_1.edge_id in result
            assert edge_2.edge_id in result

    def test_nodes_ids__from__node_id(self):                                     # Test connected node IDs
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            node_3 = Schema__MGraph__Node().set_node_type()

            edge_1 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_3.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            result = _.nodes_ids__from__node_id(node_1.node_id)

            assert type(result)   is list
            assert len(result)    == 2
            assert node_2.node_id in result
            assert node_3.node_id in result

    def test_get_node_connected_to_node__outgoing(self):                         # Test outgoing connected node by edge type
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.get_node_connected_to_node__outgoing(node_1.node_id, 'Schema__MGraph__Edge')

            assert result == node_2.node_id

    def test_get_node_connected_to_node__outgoing__not_found(self):              # Test when no connection exists
        with self.mgraph_index as _:
            node = Schema__MGraph__Node().set_node_type()
            _.add_node(node)

            result = _.get_node_connected_to_node__outgoing(node.node_id, 'Schema__MGraph__Edge')

            assert result is None

    def test_get_edge_predicate(self):                                           # Test getting predicate for edge
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(predicate=Safe_Id('my_predicate'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.get_edge_predicate(edge.edge_id)

            assert result == Safe_Id('my_predicate')

    def test_get_edge_predicate__not_found(self):                                # Test with edge without predicate
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.get_edge_predicate(edge.edge_id)

            assert result is None


    # =============================================================================
    # Edge Removal with All Label Types Tests
    # =============================================================================


    def test_remove_edge__cleans_all_label_indexes(self):                        # Test all label indexes cleaned
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(predicate = Safe_Id('the_pred'    ),
                                                     incoming  = Safe_Id('the_incoming'),
                                                     outgoing  = Safe_Id('the_outgoing'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     ,
                                              edge_path    = Edge_Path("edge.path"))

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            assert 'the_pred'     in _.index_data.labels.edges_by_predicate
            assert 'the_incoming' in _.index_data.labels.edges_by_incoming_label
            assert 'the_outgoing' in _.index_data.labels.edges_by_outgoing_label
            assert Edge_Path("edge.path") in _.index_data.paths.edges_by_path

            _.remove_edge(edge)

            assert 'the_pred'     not in _.index_data.labels.edges_by_predicate
            assert 'the_incoming' not in _.index_data.labels.edges_by_incoming_label
            assert 'the_outgoing' not in _.index_data.labels.edges_by_outgoing_label
            assert edge.edge_id   not in _.index_data.labels.edges_predicates
            assert Edge_Path("edge.path") not in _.index_data.paths.edges_by_path

    def test_remove_node__cleans_path_index(self):                               # Test path index cleaned on node removal
        with self.mgraph_index as _:
            node = Schema__MGraph__Node(node_path=Node_Path("to.remove"))
            _.add_node(node)

            assert Node_Path("to.remove") in _.index_data.paths.nodes_by_path

            _.remove_node(node)

            assert Node_Path("to.remove") not in _.index_data.paths.nodes_by_path