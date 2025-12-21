from unittest                                 import TestCase
from mgraph_db.mgraph.actions.MGraph__Data    import MGraph__Data
from mgraph_db.mgraph.actions.MGraph__Edit    import MGraph__Edit
from mgraph_db.mgraph.MGraph                  import MGraph
from mgraph_db.mgraph.index.MGraph__Index     import MGraph__Index


class test_MGraph(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graph = MGraph()

    def test_data(self):
        with self.graph.data() as _:
            assert type(_) is MGraph__Data
            assert _.graph == self.graph.graph

    def test_edit(self):
        with self.graph.edit() as _:
            assert type(_) is MGraph__Edit
            assert _.graph == self.graph.graph

    def test_index(self):
        with self.graph.index() as _:
            assert type(_) is MGraph__Index