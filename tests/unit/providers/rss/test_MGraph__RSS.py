from unittest                                               import TestCase
from typing                                                 import Dict, Any
from datetime                                               import datetime, timezone
from mgraph_db.providers.json.actions.MGraph__Json__Query   import MGraph__Json__Query
from mgraph_db.providers.json.actions.MGraph__Json__Query__Export__View import MGraph__Json__Query__Export__View
from osbot_utils.helpers.duration.Duration import Duration
from osbot_utils.utils.Files                                import file_exists, file_delete
from osbot_utils.utils.Env                                  import load_dotenv
from osbot_utils.helpers.xml.rss.RSS__Feed                  import RSS__Feed
from mgraph_db.providers.rss.MGraph__RSS__Test_Data         import MGraph__RSS__Test_Data
from osbot_utils.helpers.xml.rss.RSS__Feed__Parser          import RSS__Feed__Parser
from mgraph_db.providers.rss.MGraph__RSS                    import MGraph__RSS
from mgraph_db.providers.json.MGraph__Json                  import MGraph__Json

class test_MGraph_RSS(TestCase):

    @classmethod
    def setUpClass(cls):
        import pytest
        pytest.skip("Fix tests once MGraph_RSS is fixed")

    def setUp(self):
        self.test_data  = MGraph__RSS__Test_Data().test_rss_data()
        self.rss_feed   = RSS__Feed__Parser().from_dict(self.test_data)
        self.mgraph_json = MGraph__Json()
        self.mgraph_rss  = MGraph__RSS(graph=self.mgraph_json)
        self.mgraph_rss.load_rss(self.rss_feed)

    def test__setUp(self):
        with self.mgraph_rss as _:
            assert type(_)       is MGraph__RSS
            assert type(_.graph) is MGraph__Json
            _.graph.query().print_stats()


    def test__navigate_rss_feed(self):
        with self.mgraph_rss.graph.query() as _:
            assert type(_) is MGraph__Json__Query
            _.field('items')
            _.add_outgoing_edges__with_depth(2)
            #_.add_outgoing_edges__with_field ('title')


            export_view = MGraph__Json__Query__Export__View(mgraph_query=_)
            domain_graph_exported = export_view.export()
            mgraph_json__exported = MGraph__Json(graph=domain_graph_exported)

            mgraph_json__exported.screenshot().save().dot()
            mgraph_json__exported.export().print__dict()
        #self.mgraph_json.screenshot().save().dot()

    def test__render_as_dot(self):
        with self.mgraph_rss as _:
            target_file = './dot.png'
            _.graph.screenshot().save_to(target_file).dot()                 # this is working quite well
            #_.graph.screenshot().save_to(target_file).matplotlib()         # BUG, this is not working
            assert file_exists(target_file) is True
            assert file_delete(target_file) is True

    def test_init(self):                                                  # Test initialization
        self.assertIsInstance(self.mgraph_rss         , MGraph__RSS  )
        self.assertIsInstance(self.mgraph_rss.rss_feed, RSS__Feed)
        self.assertIsInstance(self.mgraph_rss.graph   , MGraph__Json)

    def test_properties(self):                                            # Test property access
        self.assertEqual(self.mgraph_rss.title      , 'Test RSS Feed')
        self.assertEqual(self.mgraph_rss.description, 'Test RSS Feed')
        self.assertEqual(len(self.mgraph_rss.items) , 2              )

    def test_find_items_by_category(self):                               # Test category search
        security_items = self.mgraph_rss.find_items_by_category('security')
        self.assertEqual(len(security_items), 2)

        identity_items = self.mgraph_rss.find_items_by_category('identity')
        self.assertEqual(len(identity_items), 1)
        self.assertEqual(identity_items[0]['guid'], 'test-guid-001')

    def test_find_items_by_date_range(self):                             # Test date range search
        start_date = datetime.fromtimestamp(1737627800, tz=timezone.utc)
        end_date   = datetime.fromtimestamp(1737631300, tz=timezone.utc)

        items = self.mgraph_rss.find_items_by_date_range(start_date, end_date)
        self.assertEqual(len(items), 2)

    def test_find_items_by_author(self):                                 # Test author search
        items = self.mgraph_rss.find_items_by_author('test_author')
        self.assertEqual(len(items), 2)

        items = self.mgraph_rss.find_items_by_author('non_existent')
        self.assertEqual(len(items), 0)

    def test_get_all_categories(self):                                   # Test category listing
        categories = self.mgraph_rss.get_all_categories()
        self.assertEqual(set(categories), {'security', 'identity', 'vulnerability'})

    def test_get_item_by_guid(self):                                     # Test GUID lookup
        item = self.mgraph_rss.get_item_by_guid('test-guid-001')
        self.assertIsNotNone(item)
        self.assertEqual(item['title'], 'Test Article 1')

        item = self.mgraph_rss.get_item_by_guid('non-existent')
        self.assertIsNone(item)

    def test_to_json(self):                                              # Test JSON export
        json_str = self.mgraph_rss.to_json()
        self.assertIsInstance(json_str, str)
        self.assertIn('Test RSS Feed', json_str)
        self.assertIn('test-guid-001', json_str)

    def test_to_rss(self):                                               # Test RSS export
        with self.assertRaises(NotImplementedError):
            self.mgraph_rss.to_rss()

    def test_performance(self):                                          # Test performance
        self.mgraph_rss.get_all_categories()
        self.mgraph_rss.find_items_by_category('security')
        self.mgraph_rss.find_items_by_author('test_author')
        self.mgraph_rss.to_json()