from unittest                                                           import TestCase
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict  import Schema__MGraph__Json__Node__Dict
from osbot_utils.utils.Objects                                          import type_full_name
from osbot_utils.testing.__                                             import __
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node         import Domain__MGraph__Json__Node
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Dict   import Domain__MGraph__Json__Node__Dict


class test_Domain__MGraph__Json__Node__Dict(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Initialize test data
        cls.domain_graph     = Domain__MGraph__Json__Node()
        cls.domain_node_dict = Domain__MGraph__Json__Node__Dict(graph=cls.domain_graph.graph)
        cls.domain_graph.add_node(cls.domain_node_dict.node)

    def test__init__(self):                                                                 # Test basic initialization
        with self.domain_node_dict as _:
            assert type(_)                                   is Domain__MGraph__Json__Node__Dict
            assert isinstance(_, Domain__MGraph__Json__Node) is True
            assert _.obj() == __(node  = __(data=__(node_data  = __()                                             ,
                                                    node_id    = _.node_id                                        ,
                                                    node_type  = type_full_name(Schema__MGraph__Json__Node__Dict))),
                                 graph = _.graph.obj())

    def test_add_property(self):                                                                    # Test property management with new behavior after performance fix

        with self.domain_node_dict as _:                                                            # Access domain dictionary node with context manager
            assert len(_.graph.nodes_ids()) == 1                                                    # Initially only have the dict node
            assert len(_.graph.edges_ids()) == 0                                                    # No edges in empty dict

            assert _.properties() == {}                                                             # Fresh dict has no properties
            _.add_property("test_key", "test_value")                                                # Add first property - creates new property and value nodes
            assert _.properties()               == {'test_key'   : 'test_value' }                   # Verify first property was added correctly
            _.add_property("another_key", 42)                                                       # Add second property - also creates new nodes
            assert _.properties()               == {'another_key': 42           ,                   # Verify both properties present
                                                    'test_key'   : 'test_value' }                   # Properties maintain insertion order

            assert len(_.graph.nodes_ids()) == 5                                                    # Have 5 nodes: dict + 2 property nodes + 2 value nodes
            assert len(_.graph.edges_ids()) == 4                                                    # Have 4 edges: 2 dict->property + 2 property->value

            _.add_property("test_key", 'changed')                                                   # Update creates new nodes instead of modifying existing

            assert _.properties()               == {'another_key': 42        ,                      # Properties show most recent value
                                                    'test_key'   : 'changed' }                      # Previous value exists in graph but isn't visible

            assert len(_.graph.nodes_ids()) == 7                                                    # BUG: (should be 5) : Now 7 nodes: added new property + value nodes
            assert len(_.graph.edges_ids()) == 6                                                    # BUG: (should be 4) :Now 6 edges: added new property connections

            assert _.delete_property("test_key")    is True                                         # First delete removes one property node
            assert _.properties()                   == {'another_key': 42, 'test_key': 'changed'}   # BUG: Other instance still visible
            assert _.delete_property("test_key")    is True                                         # BUG: Second delete needed for new property node
            assert _.delete_property("test_key")    is False                                        # Third delete fails - all instances removed
            assert _.properties()                   == {'another_key': 42}                          # Only other property remains
            assert _.delete_property("another_key") is True                                         # Remove final property
            assert _.delete_property("another_key") is False                                        # Verify property fully removed
            assert _.properties()                   == {}                                           # Dictionary is empty again

            assert len(_.graph.nodes_ids()) == 4                                                    # Still have 4 nodes due to undeleted value nodes
            assert len(_.graph.edges_ids()) == 0                                                    # All edges have been cleaned up

            assert self.domain_node_dict.node_id in _.graph.nodes_ids()                             # Original dictionary node still exists



    def test_delete_property(self):
        with self.domain_node_dict as _:# Test property access
            _.add_property("key1", "value1")
            _.add_property("key2", "value2")

            assert _.property("key1"        ) == "value1"
            assert _.property("key2"        ) == "value2"
            assert _.property("non_existent") is None
            assert _.delete_property("key1" ) is True
            assert _.delete_property("key1" ) is False
            assert _.delete_property("key2" ) is True
            assert _.delete_property("key2" ) is False
            assert _.delete_property("aaaaa") is False
            assert _.properties() == {}


    def test_update(self):                                                           # Test bulk property updates
        with self.domain_node_dict as _:
            test_props = { "key1": "value1" ,
                            "key2": 42      ,
                            "key3": True    }
            _.update(test_props)

            assert _.properties() == test_props