from unittest                                                               import TestCase
from mgraph_db.mgraph.domain.Domain__MGraph__Node                           import Domain__MGraph__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property  import Schema__MGraph__Json__Node__Property
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.utils.Objects                                              import type_full_name, base_types
from osbot_utils.testing.__                                                 import __
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node             import Domain__MGraph__Json__Node
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Property   import Domain__MGraph__Json__Node__Property


class test_Domain__MGraph__Json__Node__Property(TestCase):

    @classmethod
    def setUpClass(cls):  # Initialize test data
        cls.domain_node_property = Domain__MGraph__Json__Node__Property()

    def test__init__(self):                                                                 # Test basic initialization
        with self.domain_node_property as _:
            assert type(_)                                   is Domain__MGraph__Json__Node__Property
            assert base_types(_)                              == [Domain__MGraph__Json__Node, Domain__MGraph__Node, Type_Safe, object]
            assert isinstance(_, Domain__MGraph__Json__Node) is True
            assert _.obj() == __(node  = __(data=__(node_data  = __(name='')                                                  ,
                                                    node_id    = _.node_id                                             ,
                                                    node_type  = type_full_name(Schema__MGraph__Json__Node__Property))),
                                 graph = _.graph.obj())

    def test_property_name(self):                                                        # Test property name handling
        property_name = "test_property"
        node          = Domain__MGraph__Json__Node__Property(name=property_name)
        assert node.name == property_name