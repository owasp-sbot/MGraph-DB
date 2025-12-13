from unittest                                                                         import TestCase
from osbot_utils.testing.__                                                           import __
from osbot_utils.utils.Objects                                                        import base_classes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id       import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label    import Safe_Str__Label

from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                                        import PlantUML__Config
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                                        import PlantUML__Config__Graph
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                                        import PlantUML__Config__Node
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                                        import PlantUML__Config__Edge
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config                                        import PlantUML__Config__Display
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Format__Generator                             import PlantUML__Format__Generator


class test_PlantUML__Format__Generator(TestCase):

    @classmethod
    def setUpClass(cls):                                                              # shared test config
        cls.config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

    def test__init__(self):                                                           # test auto-initialization
        with PlantUML__Format__Generator() as _:
            assert type(_)                  is PlantUML__Format__Generator
            assert base_classes(_)          == [Type_Safe, object]
            assert _.config                 is None                                   # no config by default

    def test_start_uml(self):                                                         # test @startuml directive
        with PlantUML__Format__Generator(config=self.config) as _:
            assert _.start_uml()            == '@startuml'

    def test_end_uml(self):                                                           # test @enduml directive
        with PlantUML__Format__Generator(config=self.config) as _:
            assert _.end_uml()              == '@enduml'

    def test_graph_directives__default(self):                                         # test default (TB) direction
        with PlantUML__Format__Generator(config=self.config) as _:
            directives = _.graph_directives()
            assert directives               == []                                     # TB is default, no directive

    def test_graph_directives__left_to_right(self):                                   # test LR direction
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph(direction='LR')                      ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )
        with PlantUML__Format__Generator(config=config) as _:
            directives = _.graph_directives()
            assert 'left to right direction' in directives

    def test_graph_directives__right_to_left(self):                                   # test RL direction
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph(direction='RL')                      ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )
        with PlantUML__Format__Generator(config=config) as _:
            directives = _.graph_directives()
            assert 'right to left direction' in directives

    def test_graph_directives__bottom_to_top(self):                                   # test BT direction
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph(direction='BT')                      ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )
        with PlantUML__Format__Generator(config=config) as _:
            directives = _.graph_directives()
            assert 'bottom to top direction' in directives

    def test_graph_directives__with_title(self):                                      # test title directive
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph(title=Safe_Str__Label('Test Graph')) ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )
        with PlantUML__Format__Generator(config=config) as _:
            directives = _.graph_directives()
            assert 'title Test Graph' in directives

    def test_skin_params__default(self):                                              # test default skin params
        with PlantUML__Format__Generator(config=self.config) as _:
            params = _.skin_params()
            assert 'skinparam backgroundColor transparent' in params                  # always transparent
            assert 'skinparam shadowing false'             in params                  # shadowing off by default

    def test_skin_params__with_shadowing(self):                                       # test shadowing enabled
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph(shadowing=True)                      ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )
        with PlantUML__Format__Generator(config=config) as _:
            params = _.skin_params()
            assert 'skinparam shadowing false' not in params                          # not present when enabled

    def test_skin_params__with_background(self):                                      # test explicit background
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph(background_color=Safe_Str__Id('white')),
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )
        with PlantUML__Format__Generator(config=config) as _:
            params = _.skin_params()
            assert 'skinparam backgroundColor white' in params
