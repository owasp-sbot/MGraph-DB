from unittest                                                          import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id       import is_obj_id
from mgraph_db.mgraph.domain.Domain__MGraph__Node                      import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data              import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data               import Schema__MGraph__Node__Data
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Edge        import Domain__MGraph__Json__Edge
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node        import Domain__MGraph__Json__Node
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Dict  import Domain__MGraph__Json__Node__Dict
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__List  import Domain__MGraph__Json__Node__List
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Value import Domain__MGraph__Json__Node__Value
from mgraph_db.providers.json.models.Model__MGraph__Json__Edge         import Model__MGraph__Json__Edge
from mgraph_db.providers.json.models.Model__MGraph__Json__Node         import Model__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Edge       import Schema__MGraph__Json__Edge
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph      import Schema__MGraph__Json__Graph
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node       import Schema__MGraph__Json__Node
from osbot_utils.testing.__                                            import __
from osbot_utils.type_safe.Type_Safe                                   import Type_Safe
from osbot_utils.utils.Objects                                         import full_type_name, base_classes
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                     import Domain__MGraph__Graph
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph       import Domain__MGraph__Json__Graph


class test_Domain__MGraph__Json__Graph(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graph = Domain__MGraph__Json__Graph()

    def test__init__(self):
        with self.graph as _:
            assert isinstance(_, Domain__MGraph__Graph)
            assert _.obj() == __(domain_types = __(node_domain_type = full_type_name(Domain__MGraph__Json__Node),
                                                   edge_domain_type = full_type_name(Domain__MGraph__Json__Edge)),
                                 graph_type   = full_type_name(Domain__MGraph__Json__Graph)                            ,
                                 model        = __(data             = __(schema_types    = __(edge_type        = full_type_name(Schema__MGraph__Json__Edge   ),
                                                                                              graph_data_type  = full_type_name(Schema__MGraph__Graph__Data  ),
                                                                                              node_type        = full_type_name(Schema__MGraph__Json__Node   ),
                                                                                              node_data_type   = full_type_name(Schema__MGraph__Node__Data   )),
                                                                         edges           = __()             ,
                                                                         graph_data      = __(root_id=None) ,
                                                                         graph_id        = _.graph_id()     ,
                                                                         graph_type      = full_type_name(Schema__MGraph__Json__Graph),
                                                                         nodes           = __()),
                                                  model_types       = __(node_model_type = full_type_name(Model__MGraph__Json__Node),
                                                                         edge_model_type = full_type_name(Model__MGraph__Json__Edge)))) != __()

    def test_new_node(self):
        with self.graph.new_node() as _:
            assert type(_) is Domain__MGraph__Json__Node

    def test_new_edge(self):
        node_1 = self.graph.new_node()
        node_2 = self.graph.new_node()
        assert type(node_1) is Domain__MGraph__Json__Node
        assert type(node_2) is Domain__MGraph__Json__Node
        with self.graph.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id) as _:
            assert type(_) is Domain__MGraph__Json__Edge
            assert type(_.from_node()) == Domain__MGraph__Json__Node
            assert type(_.to_node  ()) == Domain__MGraph__Json__Node
            assert _.from_node_id()    == node_1.node_id
            assert _.to_node_id  ()  == node_2.node_id


    def test_root_node(self):                                                                                   # Test comprehensive root node behavior and constraints
        with Domain__MGraph__Json__Graph() as _:
            assert type(_)                         is Domain__MGraph__Json__Graph                      # Verify correct graph type
            assert _.model.data.graph_data.root_id is None                                            # Verify no root exists initially
            assert _.nodes_ids()                   == []                                              # Verify graph starts empty
            assert _.root_content()                is None                                            # Verify no content attached to root

            root    = _.root()                                                                        # Create root node on first access
            root_id = root.node_id                                                                             # Store root ID for validations

            assert is_obj_id(root_id)                           is True                                        # Validate root has proper GUID
            assert _.nodes_ids()                                == [root_id]                                   # Verify root added to graph nodes
            assert isinstance(root, Domain__MGraph__Json__Node) is True                                        # Confirm correct root node type
            assert base_classes(root)                           == [Domain__MGraph__Node, Type_Safe, object]   # Validate inheritance chain
            assert _.model.data.graph_data.root_id              == root.node_id                                # Verify root ID properly stored

            root_2 = _.root()                                                                                   # Request root node again
            assert root_2.node_id                               == root_id                                      # Verify same root returned
            assert len(_.model.node__to_edges(root_id))         == 0                                            # Verify no incoming edges allowed
            assert len(_.model.node__from_edges(root_id))       <= 1                                            # Verify maximum one outgoing edge

            # Initially no content
            assert _.root_content() is None                                                                     # confirm that it has no content

    def test_root_with_value(self):                                                         # Test root with value content
        test_value = "test_string"                                                          # new root value
        content    = self.graph.set_root_content(test_value)                                # assign it to root

        assert type(content) is  Domain__MGraph__Json__Node__Value                          # confirm that type is a Node__Value
        assert content.value == test_value

        root_content = self.graph.root_content()                                            # get the content node again

        assert isinstance(root_content, Domain__MGraph__Json__Node__Value)                  # confirm type
        assert root_content.node_id                    == content.node_id                   # confirm is the same as the created in the previous step
        assert root_content.value                      == test_value
        assert self.graph.delete_node(content.node_id) is True                              # delete root content
        assert self.graph.root_content()               is None                              # confirm it is not there

    def test_root_with_list(self):                                                          # Test root with list content
        test_list = [1, "two", True]
        content = self.graph.set_root_content(test_list)

        assert isinstance(content, Domain__MGraph__Json__Node__List)

        assert content.items() == test_list

        root_content = self.graph.root_content()                                            # Verify through root_content
        assert type(root_content)    is Domain__MGraph__Json__Node__List
        assert root_content.node_id  == content.node_id
        assert root_content.items()  == test_list

    def test_root_with_dict(self):                                                          # Test root with dict content
        test_dict = {"key1": "value1", "key2": 42}
        content = self.graph.set_root_content(test_dict)

        assert isinstance(content, Domain__MGraph__Json__Node__Dict)
        assert content.properties() == test_dict

        # Verify through root_content
        root_content = self.graph.root_content()
        assert isinstance(root_content, Domain__MGraph__Json__Node__Dict)
        assert root_content.node_id      == content.node_id
        assert root_content.properties() == test_dict

    def test_change_root_content(self):                                                     # Test changing root content
        # Start with a value
        self.graph.set_root_content("initial")
        assert isinstance(self.graph.root_content(), Domain__MGraph__Json__Node__Value)

        # Change to list
        list_content = [1, 2, 3]
        self.graph.set_root_content(list_content)
        content = self.graph.root_content()
        assert isinstance(content, Domain__MGraph__Json__Node__List)
        assert content.items() == list_content

        # Change to dict
        dict_content = {"key": "value"}
        self.graph.set_root_content(dict_content)
        content = self.graph.root_content()
        assert isinstance(content, Domain__MGraph__Json__Node__Dict)
        assert content.properties() == dict_content

    def test_complex_json_structure(self):                                                  # Test complex JSON structure
        test_data = {
            "string": "value",
            "number": 42,
            "object": {
                "nested": True,
                "list": [1, 2, {"item": "value"}]
            },
            "array": ["a", "b", {"key": "value"}]
        }

        content = self.graph.set_root_content(test_data)
        assert isinstance(content, Domain__MGraph__Json__Node__Dict)
        assert content.properties() == test_data

        # Verify through root_content
        root_content = self.graph.root_content()
        assert isinstance(root_content, Domain__MGraph__Json__Node__Dict)
        assert root_content.node_id == content.node_id
        assert root_content.properties() == test_data

