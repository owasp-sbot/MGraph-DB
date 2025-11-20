from unittest                                                           import TestCase
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph        import Domain__MGraph__Json__Graph
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__List  import Schema__MGraph__Json__Node__List
from osbot_utils.utils.Objects                                          import type_full_name
from osbot_utils.testing.__                                             import __
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node         import Domain__MGraph__Json__Node
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__List   import Domain__MGraph__Json__Node__List

class test_Domain__MGraph__Json__Node__List(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.domain_graph     = Domain__MGraph__Json__Graph()
        cls.domain_node_list = cls.domain_graph.new_list_node()
        cls.list_node_id     = cls.domain_node_list.node_id

    def tearDown(self):
        with self.domain_node_list as _:
            assert _.graph.nodes_ids() == [self.list_node_id]   # confirm that all list nodes
            assert _.graph.edges_ids() == []                    # and edges have been deleted

    def remove_all_nodes(self):                                         # BUG: we shouldn't need to delete the nodes like htis
        with self.domain_node_list as _:
            for node_id in _.graph.nodes_ids():
                if node_id != self.list_node_id:
                    assert _.graph.delete_node(node_id) is True

    def test__init__(self):                                              # Test basic initialization
        with self.domain_node_list as _:
            assert type(_) is Domain__MGraph__Json__Node__List
            assert isinstance(_, Domain__MGraph__Json__Node) is True
            assert _.obj() == __(node=__(data=__(node_data=__(),
                                               node_id=_.node_id,
                                               node_type=type_full_name(Schema__MGraph__Json__Node__List))),
                               graph=_.graph.obj())

    def test_add_primitive_values(self):                                 # Test adding primitive values
        with self.domain_node_list as _:
            assert _.graph.nodes_ids() == [self.list_node_id]
            assert _.graph.edges_ids() == []
            _.add("test_string")
            _.add(42          )
            _.add(True        )
            _.add(None        )
            assert _.items()           == ["test_string", 42, True, None]           # confirm 4 items added are there
            assert len(_.graph.nodes_ids()) == 5                                    # there should be 4 nodes + the list node
            assert len(_.graph.edges_ids()) == 4                                    # and 4 edges (one to each list value)
            _.clear()                                                               # clear list
            assert _.items()           == []                                        # confirm list is empty
            assert _.graph.nodes_ids() == [self.list_node_id]                       # and that all nodes have been deleted
            assert _.graph.edges_ids() == []                                        # and that all edges have been deleted

    def test_add_dict(self):                                                        # Test adding dictionary
        with self.domain_node_list as _:
            test_dict = {"key1": "value1", "key2": 42}
            assert len(_.graph.nodes_ids()) == 1                                    # initial we have 1 node
            assert len(_.graph.edges_ids()) == 0                                    # and 0 nodes
            _.add(test_dict)
            assert _.items() == [test_dict]
            assert len(_.graph.nodes_ids()) == 6                                    # now we have 5 more nodes (one for the dict and two per the 2 properties)
            assert len(_.graph.edges_ids()) == 5                                    # and 5 edges (one to the dict and two per the 2 properties)
            _.clear()                                                               # clear list
            assert _.items()                == []                                        # confirm list is empty
            assert len(_.graph.nodes_ids()) == 5                        # BUG: this should be 1 (the property values are not being deleted)
            assert len(_.graph.edges_ids()) == 2                        # BUG: this should be 0 (the property edges are not being deleted

            self.remove_all_nodes()                                     # BUG: we shouldn't need to delete the nodes like htis

    def test_add_nested_list(self):                                     # Test adding nested list
        with self.domain_node_list as _:
            test_list = [1, 2, ["a", "b"]]
            _.add(test_list)

            assert _.items() == [[1, 2, ["a", "b"]]]
            _.clear()
            assert _.items() == []

            self.remove_all_nodes()                                     # BUG: we shouldn't need to delete the nodes like htis


    def test_complex_structure(self):                                   # Test complex nested structure
        with self.domain_node_list as _:
            complex_data = ["string"                             ,
                            { "key" : "value"}                   ,
                            [ 1, 2, 3]                           ,
                            { "nested": { "a" : 1             ,
                                          "b" : [True, False] } }]
            
            for item in complex_data:
                _.add(item)
            
            items = _.items()
            assert len(items)               == 4
            assert items                    == complex_data
            assert len(_.graph.nodes_ids()) == 18                                   # we should have 12 nodes
            assert len(_.graph.edges_ids()) == 17                                   # and 11 edges

            _.clear()
            assert _.items() == []

            self.remove_all_nodes()                                                     # BUG: we shouldn't need to delete the nodes like htis

    def test_clear(self):                                              # Test clearing all items
        with self.domain_node_list as _:
            _.add("value1")
            _.add({"key": "value"})
            _.add([1, 2, 3])
            
            assert len(_.items()) == 3
            _.clear()
            assert len(_.items()) == 0

            self.remove_all_nodes()                                     # BUG: we shouldn't need to delete the nodes like htis

    def test_extend(self):                                             # Test extending with multiple items
        with self.domain_node_list as _:
            items = ["string", 42, {"key": "value"}, [1, 2, 3]]
            _.extend(items)
            
            assert _.items() == items

            self.remove_all_nodes()                                    # BUG: we shouldn't need to delete the nodes like htis

    def test_remove(self):                                             # Test removing items
        with self.domain_node_list as _:
            _.add("value1")
            _.add("value2")
            _.add("value1")  # Duplicate value
            
            assert _.remove("value1")    is True
            items = _.items()
            assert len(items)            == 2
            assert items.count("value1") == 1
            assert items ==  ['value2', 'value1']
            
            # Try removing non-existent value
            assert _.remove("non_existent") is False

            _.clear()
            assert _.items() == []