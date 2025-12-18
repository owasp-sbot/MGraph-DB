from unittest                                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                import PlantUML__Config__Display, PlantUML__Config__Edge, PlantUML__Config__Node, PlantUML__Config, PlantUML__Config__Graph
from osbot_utils.testing.__                                                             import __
from osbot_utils.utils.Objects                                                          import base_classes


class test_PlantUML__Config__Display(TestCase):

    def test__init__(self):                                                           # test auto-initialization
        with PlantUML__Config__Display() as _:
            assert type(_)                  is PlantUML__Config__Display
            assert base_classes(_)          == [Type_Safe, object]
            assert _.show_node_id           == False                                  # verify defaults
            assert _.show_node_type         == True
            assert _.show_node_value        == True
            assert _.show_edge_predicate    == True
            assert _.show_edge_type         == False
            assert _.wrap_at                == 40

    def test__init____with_custom_values(self):                                       # test custom initialization
        with PlantUML__Config__Display(show_node_id    = True  ,
                                       show_node_type  = False ,
                                       wrap_at         = 60    ) as _:
            assert _.show_node_id           == True
            assert _.show_node_type         == False
            assert _.wrap_at                == 60

    def test_obj(self):                                                               # test .obj() for comprehensive comparison
        with PlantUML__Config__Display() as _:
            assert _.obj() == __(show_node_id        = False ,
                                 show_node_type      = True  ,
                                 show_node_value     = True  ,
                                 show_edge_predicate = True  ,
                                 show_edge_type      = False ,
                                 wrap_at             = 40    )


class test_PlantUML__Config__Node(TestCase):

    def test__init__(self):                                                           # test auto-initialization
        with PlantUML__Config__Node() as _:
            assert type(_)                  is PlantUML__Config__Node
            assert base_classes(_)          == [Type_Safe, object]
            assert _.shape                  == 'card'                                 # verify default shape
            assert _.default_color          is None                                   # no default color
            assert _.type_colors            == {}                                     # empty dict (auto-initialized)

    def test__init____with_custom_shape(self):                                        # test shape Literal validation
        with PlantUML__Config__Node(shape='rectangle') as _:
            assert _.shape                  == 'rectangle'

        with PlantUML__Config__Node(shape='component') as _:
            assert _.shape                  == 'component'

        with PlantUML__Config__Node(shape='actor') as _:
            assert _.shape                  == 'actor'

    def test_type_colors(self):                                                       # test type color mapping
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
        with PlantUML__Config__Node() as _:
            _.type_colors['Node__Value']    = Safe_Str__Id('LightGreen')
            _.type_colors['Node__Person']   = Safe_Str__Id('LightYellow')
            assert _.type_colors['Node__Value']  == 'LightGreen'
            assert _.type_colors['Node__Person'] == 'LightYellow'


class test_PlantUML__Config__Edge(TestCase):

    def test__init__(self):                                                           # test auto-initialization
        with PlantUML__Config__Edge() as _:
            assert type(_)                  is PlantUML__Config__Edge
            assert base_classes(_)          == [Type_Safe, object]
            assert _.style                  == '-->'                                  # default arrow style
            assert _.default_color          is None
            assert _.predicate_colors       == {}

    def test__init____with_custom_style(self):                                        # test style Literal validation
        with PlantUML__Config__Edge(style='..>') as _:
            assert _.style                  == '..>'

        with PlantUML__Config__Edge(style='--|>') as _:
            assert _.style                  == '--|>'


class test_PlantUML__Config__Graph(TestCase):

    def test__init__(self):                                                           # test auto-initialization
        with PlantUML__Config__Graph() as _:
            assert type(_)                  is PlantUML__Config__Graph
            assert base_classes(_)          == [Type_Safe, object]
            assert _.direction              == 'TB'                                   # default top-to-bottom
            assert _.title                  is None
            assert _.background_color       is None
            assert _.shadowing              == False

    def test__init____with_direction(self):                                           # test direction Literal validation
        with PlantUML__Config__Graph(direction='LR') as _:
            assert _.direction              == 'LR'

        with PlantUML__Config__Graph(direction='BT') as _:
            assert _.direction              == 'BT'

    def test__init____with_title(self):                                               # test title assignment
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label import Safe_Str__Label
        with PlantUML__Config__Graph(title=Safe_Str__Label('My Graph')) as _:
            assert _.title                  == 'My Graph'


class test_PlantUML__Config(TestCase):

    def test__init__(self):                                                           # test main config container
        with PlantUML__Config() as _:
            assert type(_)                  is PlantUML__Config
            assert base_classes(_)          == [Type_Safe, object]
            assert type(_.graph)            is PlantUML__Config__Graph                # nested configs auto-init
            assert type(_.node)             is PlantUML__Config__Node
            assert type(_.edge)             is PlantUML__Config__Edge
            assert type(_.display)          is PlantUML__Config__Display

    def test__init____nested_defaults(self):                                          # verify nested config defaults
        with PlantUML__Config() as _:
            assert _.graph.direction        == 'TB'
            assert _.node.shape             == 'card'
            assert _.edge.style             == '-->'
            assert _.display.show_node_type == True

    def test_json_roundtrip(self):                                                    # test serialization/deserialization
        with PlantUML__Config() as _:
            _.graph.direction               = 'LR'
            _.node.shape                    = 'rectangle'
            _.display.show_node_id          = True

            json_data                       = _.json()
            restored                        = PlantUML__Config.from_json(json_data)

            assert restored.graph.direction        == 'LR'
            assert restored.node.shape             == 'rectangle'
            assert restored.display.show_node_id   == True
