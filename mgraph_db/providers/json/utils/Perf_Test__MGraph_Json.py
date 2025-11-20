from typing                                                     import Union
from osbot_utils.helpers.duration.decorators.capture_duration   import capture_duration
from osbot_utils.utils.Json                                     import json_file_create, json_file_load
from mgraph_db.providers.json.MGraph__Json                      import MGraph__Json
from osbot_utils.utils.Http                                     import GET_json
from osbot_utils.type_safe.Type_Safe                            import Type_Safe

class Model__Perf_Test__Duration(Type_Safe):
    duration__save_mgraph_json: float
    duration__get_source_json : float
    duration__mgraph_parse    : float
    duration__dot_creation    : float
    duration__total           : float

class Perf_Test__MGraph_Json(Type_Safe):
    perf_test_duration : Model__Perf_Test__Duration
    source_json        : Union[str, list, dict]
    mgraph_json        : MGraph__Json
    target_url         : str
    dot_code           : str

    def setup__get_source_json_from_url(self):
        with capture_duration() as duration:
            self.source_json = GET_json(self.target_url)
        self.perf_test_duration.duration__get_source_json = duration.seconds
        self.perf_test_duration.duration__total          += duration.seconds

        return self

    def step__create_mgraph(self):
        with capture_duration() as duration:
            self.mgraph_json.load().from_data(self.source_json)
        self.perf_test_duration.duration__dot_creation = duration.seconds
        self.perf_test_duration.duration__total       += duration.seconds
        return self

    def step__create_dot(self):
        with capture_duration() as duration:
            self.dot_code = self.mgraph_json.export().to_dot().to_string()
        self.perf_test_duration.duration__mgraph_parse = duration.seconds
        self.perf_test_duration.duration__total       += duration.seconds
        return self

    def step__save__mgraph_json(self):
        with capture_duration() as duration:
            exported__mgraph_json = self.mgraph_json.export().to__mgraph_json()
            target_file = '/tmp/mgraph.json'

            json_file_create(exported__mgraph_json, target_file)
            assert json_file_load(target_file) == exported__mgraph_json # BUG this is not working | round trip

            mgraph_json = self.mgraph_json.json()
            mgraph_2    = MGraph__Json.from_json(mgraph_json)
            json_file_create(mgraph_json    , '/tmp/mgraph_1.json')
            json_file_create(mgraph_2.json(), '/tmp/mgraph_2.json')

            #assert mgraph_2.json() == mgraph_json          # todo: see why this started failing on 26/feb/25 the label_edge=None was not being deserialised

            # #pprint(mgraph_2.export().to_dict())
            # print(mgraph_2.export().to_dot().to_string())
            # todo: review the load of json_mgraph data
            # from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph import Schema__MGraph__Json__Graph
            # mgraph_schema = Schema__MGraph__Json__Graph.from_json(exported__mgraph_json)
            # from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph import Domain__MGraph__Json__Graph
            # from mgraph_db.providers.json.models.Model__MGraph__Json__Graph import Model__MGraph__Json__Graph
            # mgraph_model  = Model__MGraph__Json__Graph(data=mgraph_schema)
            # mgraph_domain = Domain__MGraph__Json__Graph(model=mgraph_model)
            # mgraph_json   = MGraph__Json(graph=mgraph_domain)
            # pprint(mgraph_json.export().to_dot().to_string())




        self.perf_test_duration.duration__save_mgraph_json = duration.seconds
        self.perf_test_duration.duration__total           += duration.seconds           # todo add this automatically after each step


    def run_workflow__on_url(self, target_url):
        self.target_url = target_url
        (self.setup__get_source_json_from_url ()
             .step__create_mgraph             ()
             .step__create_dot                ()
             .step__save__mgraph_json         ())

    def run_workflow__on_json(self, source_json):
        self.source_json = source_json
        (self.step__create_mgraph       ()
             .step__create_dot          ()
             .step__save__mgraph_json   ())

    def print(self):
        print()
        print("----- Perf Test Results ----")
        print()
        print(f"  Target URL: {self.target_url}")
        print(f"  Nodes     : {len(self.mgraph_json.graph.nodes_ids())}")
        print(f"  Edges     : {len(self.mgraph_json.graph.edges_ids())}")
        print(f"  Dot Code  : {len(self.dot_code)}")
        print()
        print(f"duration__get_source_json : {self.perf_test_duration.duration__get_source_json}" )
        print(f"duration__mgraph_parse    : {self.perf_test_duration.duration__mgraph_parse}"    )
        print(f"duration__dot_creation    : {self.perf_test_duration.duration__dot_creation}"    )
        print(f"duration__save_mgraph_json: {self.perf_test_duration.duration__save_mgraph_json}")
        print('---------------------------------')
        print(f"duration__total          : {self.perf_test_duration.duration__total:.3f}")
        print('---------------------------------')
        print()

