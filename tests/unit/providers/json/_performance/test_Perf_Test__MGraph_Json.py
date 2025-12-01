import pytest
from unittest                                               import TestCase
from osbot_utils.helpers.duration.decorators.print_duration import print_duration
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id
from osbot_utils.utils.Env                                  import not_in_github_action
from osbot_utils.utils.Files                                import file_delete
from osbot_utils.utils.Json                                 import json_file_load, json__equals__list_and_set
from osbot_utils.utils.Http                                 import current_host_offline
from mgraph_db.providers.json.MGraph__Json                  import MGraph__Json
from osbot_utils.helpers.trace.Trace_Call                   import trace_calls

from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph import Schema__MGraph__Json__Graph
from mgraph_db.providers.json.utils.Perf_Test__MGraph_Json  import Perf_Test__MGraph_Json


URL__DBPEDIA__ZAP          = "https://dbpedia.org/data/ZAP.json"
URL__DBPEDIA__OWASP        = "https://dbpedia.org/data/OWASP.json"
URL__DBPEDIA__OWASP_ZAP    = "https://dbpedia.org/data/OWASP_ZAP.json"
URL__MY_FEEDS__HACKER_NEWS = "https://dev.myfeeds.ai/hacker-news/data-feed-current"
URL__MY_FEEDS__OPENAPI     = "https://dev.myfeeds.ai/openapi.json"

class test_Perf_Test__MGraph_Json(TestCase):

    @classmethod
    def setUpClass(cls):
        if not_in_github_action():
            pytest.skip("Only run tests in GitHub Actions")

    def setUp(self):
        self.perf_test = Perf_Test__MGraph_Json()

    def test__regression__in_to__mgraph_json(self):
        from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph import Domain__MGraph__Json__Graph
        mgraph        = MGraph__Json()
        domain_mgraph = mgraph.load().from_data(TEST_DATA__TECH_NEWS__FEED_XML_JSON)
        assert type(domain_mgraph) is Domain__MGraph__Json__Graph
        assert type(mgraph.graph.model.data) is Schema__MGraph__Json__Graph

        mgraph_model_data_json = mgraph.export().to__mgraph_json()
        for edge_id, edge_data in mgraph_model_data_json.get('edges').items():
            #assert type(edge_id) == Obj_Id      # BUG this should be str
            assert type(edge_id) == str          # FIXED this should be str

    def test__bug__run_workflow__on_json(self):
        pytest.skip("this test fails due to the test__bug__in_to__mgraph_json")
        with self.perf_test as _:
            _.run_workflow__on_json(TEST_DATA__TECH_NEWS__FEED_XML_JSON)
            assert _.perf_test_duration.duration__total < 2   # shower in GitHub Actions (locally it's around 0.5)
            # todo: see why this test is failing on label_edge=None (this is missing)
            #assert json_file_load('/tmp/mgraph_2.json') == json_file_load('/tmp/mgraph_1.json')
            file_delete('/tmp/mgraph_1.json')
            file_delete('/tmp/mgraph_2.json')

    def test_run_workflow__on_url(self):

        pytest.skip("dbpedia server started to behave erratically") # returned error message: "The web-site you are currently trying to access is under maintenance at this time"

        if current_host_offline():
            pytest.skip("Current server is offline")
        url = URL__DBPEDIA__ZAP                                                   #  0.291 sec (from  1 sec )
        #url = "https://dbpedia.org/data/OWASP.json"                              #  1.83      (1491 nodes  )
        #url = "https://dev.myfeeds.ai/openapi.json"                              #  0.8 sec   (from 70 secs)
        #url = "https://dbpedia.org/data/AI.json"                                 # 14.0 sec   (4524 nodes  )
        #url = URL__DBPEDIA__OWASP_ZAP                                            #  0.6 sec   (from 49 secs)
        #url = "https://dbpedia.org/data/Application_security.json"               #  1.3 sec   (1124 nodes  )
        #url = "https://dbpedia.org/data/General_Data_Protection_Regulation.json" # 16 sec     (5037 Nodes  )
        #url = "https://dev.myfeeds.ai/hacker-news/data-feed-current"             # 2.069      (1400 nodes  )

        with self.perf_test as _:
            _.run_workflow__on_url(url)
            _.print()
            assert _.perf_test_duration.duration__total < 6 # shower in GitHub Actions (locally it's around 1.5)

            #file_create('/tmp/mgraph-dot.txt', _.dot_code)


    @trace_calls(#include = ['*'],
                 contains=['add_property', 'add_node', 'new_edge', 'schema'],
                 show_duration=True, duration_padding=120,
                 show_class   =True,
                 #duration_bigger_than=0.1
                 )
    def test_trace(self):
        feed_start =  { 'channel': { 'description': 'Latest Technology News',
                                     'abc': 'xyz'},
                        'answer': 42,
                        'an_list': [1,2,3]}
        target_json = TEST_DATA__TECH_NEWS__FEED_XML_JSON
        target_json = feed_start
        mgraph_json = MGraph__Json()
        with print_duration(action_name='from-json'):
            mgraph_json.load().from_data(target_json)
        with print_duration(action_name='to-json'):
            round_trip = mgraph_json.export().to_dict()
        with print_duration(action_name='to-dot'):
            dot_code = mgraph_json.export().to_dot().to_string()
        #pprint(round_trip)
        #print(dot_code)
        assert json__equals__list_and_set(target_json, round_trip)



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### STATS on 17th Jan
#
# *** couple properties ***
#
#     @trace_calls(contains=['___mgraph', 'add_property', 'add_node', 'new_edge'], show_duration=True, duration_padding=100, show_class   =True)
#     def test_trace(self):
#         feed_start =  { 'channel': { 'description': 'Latest Technology News'}}
#         MGraph__Json().load().from_json(feed_start)
#
# 6ms without trace , 824ms with trace
#
# --------- CALL TRACER ----------
# Here are the 12 traces captured
#
# 📦  .Trace Session                                              819.282ms
# │   ├── 🧩️ Model__MGraph__Json__Graph.add_node                  16.551ms
# │   ├── 🔗️ Domain__MGraph__Json__Node__Dict.add_property       457.994ms
# │   │   ├── 🧩️ Model__MGraph__Json__Graph.add_node              18.997ms
# │   │   ├── 🔗️ Domain__MGraph__Json__Node__Dict.add_property   194.798ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.add_node          16.440ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.add_node          16.434ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.new_edge          54.339ms
# │   │   │   └── 🧩️ Model__MGraph__Json__Graph.new_edge          54.460ms
# │   │   ├── 🧩️ Model__MGraph__Json__Graph.new_edge              54.432ms
# │   │   └── 🧩️ Model__MGraph__Json__Graph.new_edge              54.227ms
# └────── 🧩️ Model__MGraph__Json__Graph.new_edge                  54.198ms
#
#
# *** couple feed_start properties ***
#
#     @trace_calls(contains=['___mgraph', 'add_property', 'add_node', 'new_edge'], show_duration=True, duration_padding=100, show_class   =True)
#     def test_trace(self):
#         feed_start =  { 'channel': { 'description': 'Latest Technology News',
#                                                      'extensions': {},
#                                                      'image'     : None,
#                                                      'items': []}}
#         MGraph__Json().load().from_json(feed_start)
#
# 10ms without trace , 1,497ms with trace
#
# --------- CALL TRACER ----------
# Here are the 25 traces captured
#
# 📦  .Trace Session                                            1,452.784ms
# │   ├── 🧩️ Model__MGraph__Json__Graph.add_node                  17.295ms
# │   ├── 🔗️ Domain__MGraph__Json__Node__Dict.add_property     1,136.912ms
# │   │   ├── 🧩️ Model__MGraph__Json__Graph.add_node              16.439ms
# │   │   ├── 🔗️ Domain__MGraph__Json__Node__Dict.add_property   195.198ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.add_node          16.482ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.add_node          16.491ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.new_edge          54.516ms
# │   │   │   └── 🧩️ Model__MGraph__Json__Graph.new_edge          54.768ms
# │   │   ├── 🔗️ Domain__MGraph__Json__Node__Dict.add_property   249.869ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.add_node          16.528ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.new_edge          54.999ms
# │   │   │   └── 🧩️ Model__MGraph__Json__Graph.new_edge          55.691ms
# │   │   ├── 🔗️ Domain__MGraph__Json__Node__Dict.add_property   193.600ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.add_node          16.617ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.add_node          16.540ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.new_edge          54.487ms
# │   │   │   └── 🧩️ Model__MGraph__Json__Graph.new_edge          54.317ms
# │   │   ├── 🔗️ Domain__MGraph__Json__Node__Dict.add_property   248.869ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.add_node          16.454ms
# │   │   │   ├── 🧩️ Model__MGraph__Json__Graph.new_edge          54.723ms
# │   │   │   └── 🧩️ Model__MGraph__Json__Graph.new_edge          54.472ms
# │   │   ├── 🧩️ Model__MGraph__Json__Graph.new_edge              54.534ms
# │   │   └── 🧩️ Model__MGraph__Json__Graph.new_edge              54.462ms
# └────── 🧩️ Model__MGraph__Json__Graph.new_edge                  54.271ms


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### STATS (16th Jan 2025)

# URL__DBPEDIA__ZAP "https://dbpedia.org/data/ZAP.json"
#
# ----- Pef Test Results ----
#
#   Target URL: https://dbpedia.org/data/ZAP.json
#   Nodes     : 101
#   Edges     : 100
#   Dot Code  : 14614
#
# duration__get_source_json: 0.087
# duration__mgraph_parse   : 0.88
# duration__dot_creation   : 0.28


# URL__DBPEDIA__OWASP_ZAP = "https://dbpedia.org/data/OWASP_ZAP.json"
#
# ----- Pef Test Results ----
#
#   Target URL: https://dbpedia.org/data/OWASP_ZAP.json
#   Nodes     : 686
#   Edges     : 685
#   Dot Code  : 104619
#
# duration__get_source_json: 0.152
# duration__mgraph_parse   : 36.692
# duration__dot_creation   : 11.842

# URL__MY_FEEDS_HACKER_NEWS = "https://dev.myfeeds.ai/hacker-news/data-feed-current"
#
# ----- Perf Test Results ----
#
#   Target URL: https://dbpedia.org/data/ZAP.json
#   Nodes     : 101
#   Edges     : 100
#   Dot Code  : 14614
#
# duration__get_source_json: 0.078
# duration__mgraph_parse   : 0.867
# duration__dot_creation   : 0.283
# ---------------------------------
# duration__total          : 1.228
# ---------------------------------



# URL__MY_FEEDS__OPENAPI = "https://dev.myfeeds.ai/openapi.json"
#
# ----- Pef Test Results ----
#
#   Target URL: https://dev.myfeeds.ai/openapi.json
#   Nodes     : 776
#   Edges     : 775
#   Dot Code  : 111630
#
# duration__get_source_json: 0.144
# duration__mgraph_parse   : 54.95
# duration__dot_creation   : 16.728
#
# (in 21st Jan 2025 - after major improvments to Type_Safe class object's creation.
#     the duration__dot_creation is not where it needs to be (from 16sec to 0.18 sec
#     but the duration__mgraph_parse is still high: 25.895 )
# ----- Perf Test Results ----
#
#   Target URL: https://dev.myfeeds.ai/openapi.json
#   Nodes     : 776
#   Edges     : 775
#   Dot Code  : 111630
#
# duration__get_source_json: 0.172
# duration__mgraph_parse   : 25.895
# duration__dot_creation   : 0.189
# ---------------------------------
# duration__total          : 42.820
# ---------------------------------




# target_json = TEST_DATA__TECH_NEWS__FEED_XML_JSON
#
# ----- Perf Test Results ----
#
#   Target URL:
#   Nodes     : 63
#   Edges     : 62
#   Dot Code  : 8957
#
# duration__get_source_json: 0.0
# duration__mgraph_parse   : 0.337
# duration__dot_creation   : 0.155
# ---------------------------------
# duration__total          : 0.492
# ---------------------------------





TEST_DATA__TECH_NEWS__FEED_XML_JSON = { 'channel': { 'description': 'Latest Technology News',
                                                     'extensions': {},
                                                     'image'     : None,
                                                     'items': [ { 'categories': [],
                                                                  'content': {},
                                                                  'creator': 'None',
                                                                  'description': 'Major advancement in artificial '
                                                                                 'intelligence research',
                                                                  'enclosure' : None,
                                                                  'extensions': { 'author': 'editor@technewsdaily.example.com',
                                                                                  'enclosure': { 'length': '12216320',
                                                                                                 'type': 'image/jpeg',
                                                                                                 'url': 'https://example.com/ai-image.jpg'}},
                                                                  'guid': '2e0985da-6a11-54be-b557-39402ba4a8ad',
                                                                  'link': 'https://technewsdaily.example.com/2024/12/ai-breakthrough.html',
                                                                  'pubDate': 'Wed, 04 Dec 2024 22:53:00 +0530',
                                                                  'thumbnail': {},
                                                                  'title': 'New AI Breakthrough'}],
                                                     'language'         : 'en-us',
                                                     'last_build_date'  : 'Thu, 05 Dec 2024 01:33:01 +0530',
                                                     'link'             : 'https://technewsdaily.example.com',
                                                     'title'            : 'Tech News Daily',
                                                     'update_frequency' : '1'              ,
                                                     'update_period'    : 'hourly'         },
                                        'extensions': {},
                                        'namespaces': {},
                                        'version': '2.0'}