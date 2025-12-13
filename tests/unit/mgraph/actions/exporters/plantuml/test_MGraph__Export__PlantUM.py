from unittest                                                                       import TestCase
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config            import PlantUML__Config
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Edge__Renderer    import PlantUML__Edge__Renderer
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Node__Renderer    import PlantUML__Node__Renderer
from mgraph_db.providers.simple.domain.Domain__Simple__Graph                        import Domain__Simple__Graph
from mgraph_db.mgraph.actions.exporters.plantuml.MGraph__Export__PlantUML           import MGraph__Export__PlantUML, PlantUML__Context
from mgraph_db.providers.simple.MGraph__Simple                                      import MGraph__Simple


class test_MGraph__Export__PlantUML(TestCase):
    def setUp(self):
        self.mgraph_simple   = MGraph__Simple()
        self.plantuml_export = MGraph__Export__PlantUML(graph=self.mgraph_simple.graph).setup()

    def test__setUp(self):
        with self.plantuml_export as _:
            assert type(_) is MGraph__Export__PlantUML
            assert type(_.graph            ) is Domain__Simple__Graph
            assert type(_.config           ) is PlantUML__Config
            assert type(_.context          ) is PlantUML__Context
            assert type(_.node_renderer    ) is PlantUML__Node__Renderer
            assert type(_.edge_renderer    ) is PlantUML__Edge__Renderer
            assert _.data                    is None
            assert _.index                   is None
            assert _.on_add_node             is None
            assert _.on_add_edge             is None

    def test_process_graph(self):
        with self.plantuml_export as _:
            plantuml_code = _.render()

            assert  plantuml_code      == '_startuml_skinparam backgroundColor transparent_skinparam shadowing false____enduml'
            assert type(plantuml_code) is Safe_Str__Text
