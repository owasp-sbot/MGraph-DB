from unittest                                                            import TestCase
from mgraph_db.mgraph.MGraph                                             import MGraph
from mgraph_db.mgraph.actions.exporters.tree.MGraph__Export__Tree_Values import MGraph__Export__Tree_Values
from mgraph_db.mgraph.domain.Domain__MGraph__Node                        import Domain__MGraph__Node
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Base             import Model__MGraph__Export__Context
from mgraph_db.mgraph.actions.MGraph__Builder                            import MGraph__Builder
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                       import Domain__MGraph__Graph
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id        import Node_Id


class test_MGraph__Export__Tree_Values(TestCase):

    def setUp(self):
        self.mgraph      = MGraph()
        self.builder     = MGraph__Builder            (mgraph_edit = self.mgraph.edit())
        self.export_tree = MGraph__Export__Tree_Values(graph       = self.mgraph.graph )

    def test__init__(self):
        with self.export_tree as _:
            assert type(_           ) is MGraph__Export__Tree_Values
            assert type(_.graph     ) is Domain__MGraph__Graph
            assert type(_.context   ) is Model__MGraph__Export__Context

    def create_simple_tree(self):                                               # Create a simple tree with a root node and one child
        with self.builder as _:
            root_node = _.add_node('root_node')
            root_node_id = root_node.node_id()
            _.add_connected_node(value='child_node', predicate='has child')
            return root_node_id

    def test_create_simple_tree(self):                                          # Test creating a simple tree and verify the structure
        root_node_id = self.create_simple_tree()
        root_node    = self.mgraph.data().node(root_node_id)

        with self.mgraph as _:
            assert type(_           ) is MGraph
            assert type(_.graph     ) is Domain__MGraph__Graph
            assert type(root_node   ) is Domain__MGraph__Node
            assert type(root_node_id) is Node_Id
            assert _.data().stats() == {'edges_ids': 1, 'nodes_ids': 2}
            assert root_node.node_data.value == 'root_node'

    def create_complex_tree(self):                                                  # Create a more complex tree structure for testing
        with self.builder as _:

            root_node = _.add_node('root_node')                                     # Create the root node
            root_id   = root_node.node_id()

            (_.add_connected_node(value  = 'child1'          , predicate = 'has_child'           )
              .add_connected_node(value  = 'grandchild1'     , predicate = 'has_descendant'      )
              .add_connected_node(value  = 'great_grandchild', predicate = 'has_great_descendant')
              .add_predicate     (target = root_id           , predicate =  'circular reference' )
              .up().up().up()
              .add_connected_node(value = 'grandchild2'      , predicate = 'has_descendant'      )
              .up().up().up()
              .add_connected_node(value = 'child2'           , predicate = 'has_child'           )
              .add_connected_node(value = 'grandchild3'      , predicate = 'has_descendant'      )
              .up().up()
              .add_connected_node(value = 'child3'           , predicate = 'has_child'           ))


            return root_id

    def test_complex_tree_structure(self): # Test the tree export with a more complex structure
        root_id = self.create_complex_tree()

        # with self.mgraph.screenshot() as _:
        #     load_dotenv()
        #     _.show_node_value()
        #     _.show_edge_predicate()
        #     _.save_to(f'{self.__class__.__name__}.png')
        #     _.dot()


        with self.export_tree as _:
            _.root_nodes_ids = [root_id]
            tree_output      = _.format_output()

            trees = tree_output.get('trees', [])
            assert len(trees) == 1

            root_tree = trees[0]
            assert root_tree['value'] == 'root_node'
            assert 'has_child' in root_tree['children']


            has_child_nodes = root_tree['children']['has_child']                                        # Check the first level children
            assert len(has_child_nodes) == 3                                                            # There are 3 children: child1, child2, child3


            child1 = next((child for child in has_child_nodes if child['value'] == 'child1'), None)     # Check content of first child
            assert child1 is not None
            assert 'has_descendant' in child1['children']

            text_tree = _.format_as_text(root_tree)     # check format_as_text

            assert text_tree == """\
root_node
    has_child:
        child1
            has_descendant:
                grandchild1
                    has_great_descendant:
                        great_grandchild
                            circular_reference:
                                root_node
                grandchild2
        child2
            has_descendant:
                grandchild3
        child3"""
