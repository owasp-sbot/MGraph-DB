from unittest                                                               import TestCase
from mgraph_db.mgraph.actions.exporters.plantuml.MGraph__Export__PlantUML   import MGraph__Export__PlantUML
from mgraph_db.providers.simple.MGraph__Simple__Test_Data                   import MGraph__Simple__Test_Data
from osbot_utils.utils.Env                                                  import load_dotenv

class test_MGraph__Export__Dot__screenshots(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.create_screenshot = False
        cls.screenshot_file   = './export-plantuml.png'

    def setUp(self):                                                                    # Initialize test environment
        self.simple_graph = MGraph__Simple__Test_Data().create()
        self.domain_graph = self.simple_graph.graph
        self.exporter     = MGraph__Export__PlantUML(graph=self.domain_graph)               # Create DOT exporter

    def tearDown(self):
        if self.create_screenshot:
            load_dotenv()
            # with self.simple_graph.screenshot() as _:
            #     _.save_to(self.screenshot_file).dot_to_png(self.exporter.dot_code)

    # def test_plantuml_to_png(self):
    #     print('here')
