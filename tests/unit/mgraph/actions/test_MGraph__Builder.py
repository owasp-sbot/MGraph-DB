from unittest                                       import TestCase
from mgraph_db.mgraph.MGraph                        import MGraph
from mgraph_db.mgraph.actions.MGraph__Builder       import MGraph__Builder
from mgraph_db.mgraph.domain.Domain__MGraph__Node   import Domain__MGraph__Node
from mgraph_db.mgraph.domain.Domain__MGraph__Edge   import Domain__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge  import Schema__MGraph__Edge
from osbot_utils.utils.Env                          import load_dotenv


class An_Edge(Schema__MGraph__Edge): pass

class test_MGraph__Builder(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.create_png = False

    def setUp(self):
        self.mgraph = MGraph()
        self.builder = MGraph__Builder(mgraph_edit=self.mgraph.edit())

    def tearDown(self):
        if self.create_png:
            with self.mgraph.screenshot() as _:
                with _.export().export_dot() as dot:
                    dot.set_graph__rank_dir__lr()
                    dot.set_node__shape__type__box()
                    dot.set_node__shape__rounded()
                    #dot.show_edge__type()
                    dot.show_edge__predicate__str()

                load_dotenv()
                _.save_to(f'{self.__class__.__name__}.png')
                _.show_node_value()
                _.dot()


    def test_init(self):
        assert type(self.builder) is MGraph__Builder
        assert self.builder.mgraph_edit == self.mgraph.edit()
        assert self.builder.node__current is None
        assert self.builder.node__history == []
        assert self.builder.edge__current is None
        assert self.builder.edge__history == []
        assert self.builder.node__root is None

    def test_add_node(self):
        builder = self.builder.add_node("test_node")
        assert type(builder) is MGraph__Builder
        assert type(builder.node__current) is Domain__MGraph__Node
        assert builder.node__current.node_data.value == "test_node"
        assert builder.node__root == builder.node__current

    def test_connect_to(self):
        builder = self.builder.add_node("node1").connect_to("node2")

        # Check nodes
        assert builder.node__current.node_data.value    == "node2"
        assert builder.node__history[0].node_data.value == "node1"

        # Check edges
        assert type(builder.edge__current) is Domain__MGraph__Edge
        assert builder.edge__current.from_node().node_data.value == "node1"
        assert builder.edge__current.to_node  ().node_data.value == "node2"

    def test_add_predicate(self):
        builder = self.builder.add_node("subject").add_predicate("predicate", "object")     # Define a simple edge type for testing

        # Check nodes
        assert builder.node__current.node_data.value    == "object"
        assert builder.node__history[0].node_data.value == "subject"

        # Check edges
        assert type(builder.edge__current)                          is Domain__MGraph__Edge
        assert builder.edge__current.from_node().node_data.value    == "subject"
        assert builder.edge__current.to_node().node_data.value      == "object"
        assert builder.edge__current.edge.data.edge_label.predicate == "predicate"

    def test_navigation(self):
        builder = (self.builder
                  .add_node("root")
                  .connect_to("child1")
                  .connect_to("grandchild")
                  .node_up()
                  .connect_to("child2"))

        child_2_id = builder.node__current.node_id
        # Current node should be "child2"
        assert builder.node__current.node_data.value == "child2"

        # Navigate to root
        builder.root()
        assert builder.node__current.node_data.value == "root"

        # Navigate to a specific node
        child1_id = builder.node__history[0].node_id
        builder.set_current_node(child_2_id)
        assert builder.node__current.node_data.value == "child2"

    def test_complex_graph(self):
        # Create a more complex graph
        with self.mgraph.builder() as g:
            (g.add_node("Person")
             .connect_to("John", An_Edge)
             .add_predicate("has attribute", "age")
             .connect_to(25)
             .node_up()
             .node_up()
             .add_predicate("has relationship", "Friend")
             .connect_to("Jane"))

        # Verify graph structure using data methods
        nodes = self.mgraph.data().nodes()
        assert len(nodes) == 6  # Person, John, age, 25, Friend, Jane

        edges = self.mgraph.data().edges()
        assert len(edges) == 5  # Person->John, John->age, age->25, John->Friend, Friend->Jane

        # Find the "Person" node
        person_node = None
        for node in nodes:
            if node.node_data and node.node_data.value == "Person":
                person_node = node
                break

        assert person_node is not None

        # Check connections from Person
        person_edges = self.mgraph.index().get_node_id_outgoing_edges(person_node.node_id)
        assert len(person_edges) == 1