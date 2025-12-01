import re
import pytest
from unittest                                                            import TestCase

from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List    import Type_Safe__List
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Types          import Schema__Mermaid__Types
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id         import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id        import Safe_Id
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge           import Schema__Mermaid__Edge
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge__Config   import Schema__Mermaid__Edge__Config
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph          import Schema__Mermaid__Graph
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph__Config  import Schema__Mermaid__Graph__Config
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node           import Schema__Mermaid__Node
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data     import Schema__Mermaid__Node__Data


class test_Schema__Mermaid__Graph(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.schema_types  = Schema__Mermaid__Types()
        self.graph_data    = Schema__Mermaid__Graph__Config(allow_circle_edges   = True,
                                                            allow_duplicate_edges= False,
                                                            graph_title         = "Test Graph")
        self.node          = Schema__Mermaid__Node         (node_data = Schema__Mermaid__Node__Data()     ,
                                                            node_type   = Schema__Mermaid__Node           ,
                                                            key         = Safe_Id("node_1")               ,
                                                            label       = "Test Node"                     )
        self.edge          = Schema__Mermaid__Edge         (edge_config  = Schema__Mermaid__Edge__Config(),
                                                            edge_type    = Schema__Mermaid__Edge          ,
                                                            from_node_id = Node_Id(Obj_Id())              ,
                                                            to_node_id   = Node_Id(Obj_Id())              ,
                                                            label        = "Test Edge"                    )
        self.graph          = Schema__Mermaid__Graph       (schema_types = self.schema_types              ,
                                                            edges        = {self.edge.edge_id: self.edge} ,
                                                            nodes        = {self.node.node_id: self.node} ,
                                                            graph_data   = self.graph_data                ,
                                                            graph_type   = Schema__Mermaid__Graph         ,
                                                            mermaid_code = ["graph TD", "A --> B"]        )

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.graph)              is Schema__Mermaid__Graph
        assert self.graph.graph_data         == self.graph_data
        assert len(self.graph.nodes)         == 1
        assert len(self.graph.edges)         == 1
        assert type(self.graph.mermaid_code) is Type_Safe__List
        assert len(self.graph.mermaid_code)  == 2

    def test_type_safety_validation(self):                                          # Tests type safety validations
        error_message_1 = ("On Schema__Mermaid__Graph, invalid type for attribute 'edges'. "
                         "Expected 'typing.Dict[osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id.Obj_Id, "
                         "mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge.Schema__Mermaid__Edge]' "
                         "but got '<class 'str'>'")
        with pytest.raises(ValueError, match=re.escape(error_message_1)):
            Schema__Mermaid__Graph(edges        = "not-a-dict"          ,
                                   nodes        = {}                    ,
                                   graph_data   = self.graph_data       ,
                                   graph_type   = Schema__Mermaid__Graph,
                                   mermaid_code = ["graph TD"]          )

        error_message_2 = ("On Schema__Mermaid__Graph, invalid type for attribute 'mermaid_code'. "
                           "Expected 'typing.List[str]' but got '<class 'str'>'")
        with pytest.raises(ValueError, match=re.escape(error_message_2)):

            Schema__Mermaid__Graph(edges        = {}                    ,
                                   nodes        = {}                    ,
                                   graph_data   = self.graph_data       ,
                                   graph_type   = Schema__Mermaid__Graph,
                                   mermaid_code = "not-a-list"          )


