from unittest                                                           import TestCase

import pytest

from mgraph_db.providers.mermaid.MGraph__Mermaid                        import MGraph__Mermaid
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Diagram__Type import Schema__Mermaid__Diagram__Type
from mgraph_db.providers.mermaid.utils.Mermaid_Examples__FlowChart      import Mermain_Examples__FlowChart
from osbot_utils.testing.Pytest import skip_pytest
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id       import Safe_Id
from osbot_utils.utils.Str                                              import str_dedent


class test_Mermaid_Examples__FlowChart(TestCase):


    def setUp(self):
        self.mermaid             = MGraph__Mermaid()
        self.mermaid_edit        = self.mermaid.edit()
        self.mermaid_render      = self.mermaid.render()
        self.examples            = Mermain_Examples__FlowChart()
        self.target_example      = None
        self.assert_on_exit      = True
        self.print_expected_code = False
        self.print_on_exit       = False
        self.save_on_exit        = False

    def tearDown(self):
        test_name      = self.id().split('.')[-1]                       # This will get the name of the current test method
        target_example = test_name.replace('test_','')      # Replace 'test_' with an empty string to follow your naming convention

        expected_code = self.examples.__getattribute__(target_example)
        rendered_code = self.mermaid.code()
        if self.assert_on_exit      : assert rendered_code.strip() == str_dedent(expected_code)
        if self.print_expected_code : print(f"\n______expected code______\n{expected_code}")
        if self.print_on_exit       : print(f"\n______rendered code______\n{rendered_code}")
        if self.save_on_exit        : self.mermaid.save()

    def test_example_1__a_node_default(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='id').show_label(False)

    def test_example_2__a_node_with_text(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='id1', label='This is the text in the box').wrap_with_quotes(False)

    def test_example_3__a_node_with_unicode_text(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='id', label='This ❤ Unicode')

    @pytest.mark.skip("started failing with recent removal of @type_safe decorators")  # todo: figure out what caused this
    def test_example_4__a_node_with_markdown_formatting(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_directive('init: {"flowchart": {"htmlLabels": false}} ')
            _.add_node(key='markdown', label='This **is** _Markdown_').markdown()
            _.add_node(key='newLines', label="""Line1
    Line 2
    Line 3""").markdown()
            _.add_edge('markdown', 'newLines')
            _.render_config().line_before_edges = False


    def test_example_5__direction__from_top_to_bottom(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.render_config().line_before_edges = False
            _.render_config().add_nodes         = False
            _.set_direction('TD')
            _.add_edge(Safe_Id('Start'), Safe_Id('Stop'))


    def test_example_6__direction__from_left_to_right(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.render_config().line_before_edges = False
            _.render_config().add_nodes         = False
            _.set_direction('LR')
            _.add_edge(Safe_Id('Start'), Safe_Id('Stop'))

    def test_example_7__node_shapes_a_node_with_round_edges(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='id1', label='This is the text in the box').shape_round_edges().wrap_with_quotes(False)

    def test_example_8__node_shapes_a_stadium_shaped_node(self):

        #self.assert_on_exit      = True
        #self.print_on_exit       = True
        #self.print_expected_code = True

        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='id1', label='This is the text in the box').shape_stadium().wrap_with_quotes(False)


    def test_example_9__node_shapes_a_node_in_a_subroutine(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='id1', label='This is the text in the box').shape_subroutine().wrap_with_quotes(False)

    def test_example_10__node_shapes_a_node_in_a_cylindrical_shape(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='id1', label='Database').shape_cylindrical().wrap_with_quotes(False)

    def test_example_11__node_shapes_a_node_in_the_form_of_a_circle(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='id1', label='This is the text in the circle').shape_circle().wrap_with_quotes(False)

    def test_example_12__node_shapes_a_node_in_an_asymmetric_shape(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='id1', label='This is the text in the box').shape_asymmetric().wrap_with_quotes(False)

    def test_example_13__node_shapes_a_node_rhombus(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='id1', label='This is the text in the box').shape_rhombus().wrap_with_quotes(False)

    def test_example_14__node_shapes_a_hexagon_node(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='id1', label='This is the text in the box').shape_hexagon().wrap_with_quotes(False)

    def test_example_15__node_shapes_parallelogram(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.set_direction('TD')
            _.add_node(key='id1', label='This is the text in the box').shape_parallelogram().wrap_with_quotes(False)

    def test_example_16__node_shapes_parallelogram_alt(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.set_direction('TD')
            _.add_node(key='id1', label='This is the text in the box').shape_parallelogram_alt().wrap_with_quotes(False)

    def test_example_17__node_shapes_trapezoid(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.set_direction('TD')
            _.add_node(key='A', label='Christmas').shape_trapezoid().wrap_with_quotes(False)

    def test_example_18__node_shapes_trapezoid_alt(self):
        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.set_direction('TD')
            _.add_node(key='B', label='Go shopping').shape_trapezoid_alt().wrap_with_quotes(False)

    def test_example_19__node_shapes_double_circle(self):

        with self.mermaid_edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.set_direction('TD')
            _.add_node(key='id1', label='This is the text in the circle').shape_double_circle().wrap_with_quotes(False)
            #_.save()

    # def test_(self):
    #
    #     self.assert_on_exit      = False
    #     self.print_on_exit       = True
    #     self.print_expected_code = True
    #
    #     with self.mermaid as _:
    #         _.set_diagram_type(Diagram__Type.flowchart)

    # def test_(self):
    #
    #     self.assert_on_exit      = False
    #     self.print_on_exit       = True
    #     self.print_expected_code = True
    #
    #     with self.mermaid as _:
    #         _.set_diagram_type(Diagram__Type.flowchart)

    # def test_(self):
    #
    #     self.assert_on_exit      = False
    #     self.print_on_exit       = True
    #     self.print_expected_code = True
    #
    #     with self.mermaid as _:
    #         _.set_diagram_type(Diagram__Type.flowchart)

    # def test_(self):
    #
    #     self.assert_on_exit      = False
    #     self.print_on_exit       = True
    #     self.print_expected_code = True
    #
    #     with self.mermaid as _:
    #         _.set_diagram_type(Diagram__Type.flowchart)


