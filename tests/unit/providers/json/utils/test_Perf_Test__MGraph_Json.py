from unittest                                               import TestCase
from mgraph_ai.providers.json.MGraph__Json                  import MGraph__Json
from osbot_utils.helpers.trace.Trace_Call                   import trace_calls
from mgraph_ai.providers.json.utils.Perf_Test__MGraph_Json  import Perf_Test__MGraph_Json


URL__DBPEDIA__ZAP          = "https://dbpedia.org/data/ZAP.json"
URL__DBPEDIA__OWASP_ZAP    = "https://dbpedia.org/data/OWASP_ZAP.json"
URL__MY_FEEDS__HACKER_NEWS = "https://dev.myfeeds.ai/hacker-news/data-feed-current"
URL__MY_FEEDS__OPENAPI     = "https://dev.myfeeds.ai/openapi.json"

class test_Perf_Test__MGraph_Json(TestCase):

    def setUp(self):
        self.perf_test = Perf_Test__MGraph_Json()

    def test_run_workflow__on_json(self):
        with self.perf_test as _:
            _.run_workflow__on_json(TEST_DATA__TECH_NEWS__FEED_XML_JSON)
            _.print()
            assert _.perf_test_duration.duration__total < 2   # shower in GitHub Actions (locally it's around 0.5)

    def test_run_workflow__on_url(self):
        url = URL__DBPEDIA__ZAP
        with self.perf_test as _:
            _.run_workflow__on_url(url)
            _.print()
            assert _.perf_test_duration.duration__total < 6 # shower in GitHub Actions (locally it's around 1.5)

    # contains=['models__from_edges', 'edges', 'add_node', 'new_dict_node', 'add_property'],
    @trace_calls(contains=['___mgraph', 'add_property', 'add_node', 'new_edge'],
                 show_duration=True, duration_padding=100,
                 show_class   =True)
    def test_trace(self):
        feed_start =  { 'channel': { 'description': 'Latest Technology News'}}
        MGraph__Json().load().from_json(feed_start)  # TEST_DATA__TECH_NEWS__FEED_XML_JSON



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
### STATS (16th Jan 2024)

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