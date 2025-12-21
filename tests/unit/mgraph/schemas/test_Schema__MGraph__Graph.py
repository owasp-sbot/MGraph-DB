import re
import pytest
from unittest                                                       import TestCase
from mgraph_db.mgraph.MGraph                                        import MGraph
from mgraph_db.utils.testing.mgraph_test_ids                        import mgraph_test_ids
from osbot_utils.testing.__                                         import __, __SKIP__
from mgraph_db.mgraph.schemas.Schema__MGraph__Types                 import Schema__MGraph__Types
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data           import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.identifiers.Graph_Path                import Graph_Path
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id  import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id


class Simple_Node(Schema__MGraph__Node): pass    # Helper class for testing

class test_Schema__MGraph__Graph(TestCase):

    def setUp(self):    # Initialize test data
        with mgraph_test_ids():
            self.schema_types  = Schema__MGraph__Types(node_type      = Simple_Node,
                                                       edge_type      = Schema__MGraph__Edge)
            self.graph_data    = Schema__MGraph__Graph__Data   ()
            self.node_data     = Schema__MGraph__Node__Data    ()
            self.node          = Schema__MGraph__Node          (node_data      = self.node_data,
                                                                node_type      = Simple_Node)
            self.edge          = Schema__MGraph__Edge          (edge_type      = Schema__MGraph__Edge,
                                                                from_node_id   = Node_Id(Obj_Id())            ,
                                                                to_node_id     = Node_Id(Obj_Id())            )
            self.graph         = Schema__MGraph__Graph         (schema_types   = self.schema_types,
                                                                edges          = {self.edge.edge_id: self.edge},
                                                                graph_data     = self.graph_data,
                                                                graph_type     = Schema__MGraph__Graph,
                                                                nodes          = {self.node.node_id: self.node} )

    def test_init(self):    # Tests basic initialization and type checking
        assert type(self.graph)                                is Schema__MGraph__Graph
        assert self.graph.graph_data == self.graph_data
        assert len(self.graph.nodes)                           == 1
        assert len(self.graph.edges)                           == 1
        assert self.graph.nodes[self.node.node_id            ] == self.node
        assert self.graph.edges[self.edge.edge_id            ] == self.edge
        assert self.graph.obj()                                == __(graph_data=__(),
                                                                     graph_path=None,
                                                                     graph_type='mgraph_db.mgraph.schemas.Schema__MGraph__Graph.Schema__MGraph__Graph',
                                                                     schema_types=__(edge_type='mgraph_db.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge',
                                                                                     graph_data_type=None,
                                                                                     node_type='test_Schema__MGraph__Graph.Simple_Node',
                                                                                     node_data_type=None),
                                                                     index_config=None,
                                                                     edges=__(e0000001=__(edge_data=None,
                                                                                          edge_type='mgraph_db.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge',
                                                                                          edge_label=None,
                                                                                          edge_path=None,
                                                                                          from_node_id='c0000002',
                                                                                          to_node_id='c0000003',
                                                                                          edge_id='e0000001')),
                                                                     graph_id='a0000001',
                                                                     nodes=__(c0000001=__(node_data=__(),
                                                                                          node_path=None,
                                                                                          node_type='test_Schema__MGraph__Graph.Simple_Node',
                                                                                          node_id='c0000001')))


    def test_type_safety_validation(self):    # Tests type safety validations
        error_message = "On Schema__MGraph__Graph, invalid type for attribute 'nodes'. Expected 'typing.Dict[osbot_utils.type_safe.primitives.domains.identifiers.Node_Id.Node_Id, mgraph_db.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node]' but got '<class 'str'>'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Schema__MGraph__Graph(nodes        = "not-a-dict",
                                  edges        = {self.edge.edge_id: self.edge},
                                  graph_config = self.graph_data,
                                  graph_type   = Schema__MGraph__Graph)

        expected_error = "Expected 'Schema__MGraph__Edge', but got 'str'"
        with pytest.raises(TypeError, match=expected_error):
            Schema__MGraph__Graph(nodes        = {self.node.node_id : self.node     },
                                  edges        = {self.edge.edge_id : "not-an-edge" },
                                  graph_config = self.graph_data                     ,
                                  graph_type   = Schema__MGraph__Graph               )

    def test_multiple_nodes_and_edges(self):    # Tests graph with multiple nodes and edges
        node_data_2   = Schema__MGraph__Node__Data  (                                    )
        node_2        = Schema__MGraph__Node        (node_data    = node_data_2          )
        edge_2        = Schema__MGraph__Edge        (edge_type    = Schema__MGraph__Edge ,
                                                     from_node_id = self.node.node_id    ,
                                                     to_node_id   = node_2.node_id       )

        graph = Schema__MGraph__Graph               (nodes        = { self.node.node_id : self.node             ,
                                                                      node_2.node_id    : node_2               },
                                                     edges        = { self.edge.edge_id : self.edge ,
                                                                      edge_2.edge_id    : edge_2   },
                                                     graph_data   = self.graph_data                             ,
                                                     graph_type   = Schema__MGraph__Graph                       )

        assert len(graph.nodes) == 2
        assert len(graph.edges) == 2

    def test_graph_with_path(self):                                                                 # Test graph creation with path
        with Schema__MGraph__Graph( graph_id     = Graph_Id()                    ,
                                    graph_type   = Schema__MGraph__Graph         ,
                                    graph_data   = Schema__MGraph__Graph__Data() ,
                                    schema_types = Schema__MGraph__Types()       ,
                                    graph_path   = Graph_Path("service.my-graph")) as _:
            assert _.graph_path      == Graph_Path("service.my-graph")
            assert str(_.graph_path) == "service.my-graph"

    def test_graph_without_path(self):                                                              # Test graph creation without path (backward compatibility)
        with Schema__MGraph__Graph( graph_id     = Graph_Id()                    ,
                                    graph_type   = Schema__MGraph__Graph         ,
                                    graph_data   = Schema__MGraph__Graph__Data() ,
                                    schema_types = Schema__MGraph__Types()       ) as _:
            assert _.graph_path is None

    def test_graph_serialization_roundtrip_with_path(self):                                         # Test that graph path survives serialization
        with Schema__MGraph__Graph( graph_id     = Graph_Id()                    ,
                                    graph_type   = Schema__MGraph__Graph         ,
                                    graph_data   = Schema__MGraph__Graph__Data() ,
                                    schema_types = Schema__MGraph__Types()       ,
                                    graph_path   = Graph_Path("test.graph.path") ) as _:
            json_data = _.json()
            restored  = Schema__MGraph__Graph.from_json(json_data)

            assert restored.graph_path      == _.graph_path
            assert str(restored.graph_path) == "test.graph.path"

    def test_graph_default_value(self):
        graph_id = 'c0787747'
        node_id  = 'adf69958'
        with Schema__MGraph__Graph(graph_id=graph_id) as _:
            assert _.obj() == __(graph_path   = None,
                                 edges        = __(),
                                 graph_data   = None, # __(),
                                 graph_id     = graph_id,
                                 graph_type   = None, #'mgraph_db.mgraph.schemas.Schema__MGraph__Graph.Schema__MGraph__Graph',
                                 nodes        = __(),
                                 schema_types = None)   #__(edge_type='mgraph_db.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge',
                                                        #   graph_data_type='mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data.Schema__MGraph__Graph__Data',
                                                        #   node_type='mgraph_db.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node',
                                                        #   node_data_type='mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data'))
        node_value = "this is a new value"
        with MGraph(graph_id=graph_id) as _:
            _.edit().new_value(node_value, node_id=node_id)
            # todo: see if we can make more values None
            assert _.obj() == __(graph=__(graph_type=None,
                                          domain_types=__(node_domain_type=None, edge_domain_type=None),
                                          model=__(data=__(graph_data=None,
                                                           graph_path=None,
                                                           graph_type=None,
                                                           schema_types=None,
                                                           edges=__(),
                                                           graph_id='c0787747',
                                                           nodes=__(adf69958=__(node_id='adf69958',
                                                                                node_type='mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value.Schema__MGraph__Node__Value',
                                                                                node_data=__(value_type = 'builtins.str',
                                                                                             value      = node_value    ,
                                                                                             key        = ''            ),
                                                                                node_path=None))),
                                                   model_types=__(node_model_type=None, edge_model_type=None),
                                                   resolver=__SKIP__),
                                          resolver=__SKIP__),
                                 query_class='mgraph_db.query.MGraph__Query.MGraph__Query',
                                 edit_class='mgraph_db.mgraph.actions.MGraph__Edit.MGraph__Edit',
                                 screenshot_class='mgraph_db.mgraph.actions.MGraph__Screenshot.MGraph__Screenshot')