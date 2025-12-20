from unittest                                                                         import TestCase
from osbot_utils.utils.Objects                                                        import base_classes
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from mgraph_db.mgraph.actions.exporters.plantuml.MGraph__Export__PlantUML                                       import PlantUML__Context

class test_PlantUML__Context(TestCase):

    def test__init__(self):                                                           # test context auto-initialization
        with PlantUML__Context() as _:
            assert type(_)                  is PlantUML__Context
            assert base_classes(_)          == [Type_Safe, object]
            assert _.nodes                  == []                                     # empty list (auto-init)
            assert _.edges                  == []                                     # empty list (auto-init)

    def test_nodes_accumulation(self):                                                # test adding to nodes
        with PlantUML__Context() as _:
            _.nodes.append('card "Test" as n1')
            _.nodes.append('card "Test2" as n2')
            assert len(_.nodes)             == 2

    def test_edges_accumulation(self):                                                # test adding to edges
        with PlantUML__Context() as _:
            _.edges.append('n1 --> n2')
            _.edges.append('n2 --> n3 : label')
            assert len(_.edges)             == 2