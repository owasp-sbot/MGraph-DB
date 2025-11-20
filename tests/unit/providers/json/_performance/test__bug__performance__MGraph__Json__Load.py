import pytest
from typing                                                                         import Any
from unittest                                                                       import TestCase
from osbot_utils.utils.Env                                                          import in_github_action
from mgraph_db.providers.json.MGraph__Json                                          import MGraph__Json
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph                    import Domain__MGraph__Json__Graph
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Dict               import Domain__MGraph__Json__Node__Dict
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property          import Schema__MGraph__Json__Node__Property
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property__Data    import Schema__MGraph__Json__Node__Property__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value             import Schema__MGraph__Json__Node__Value
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data       import Schema__MGraph__Json__Node__Value__Data
from osbot_utils.helpers.duration.decorators.capture_duration                       import capture_duration

class test__regression__performance__MGraph__Json__Load(TestCase):

    def setUp(self):                                                                        # Initialize test environment and data
        self.mgraph_json = MGraph__Json()
        self.json_data = { "string" : "value"         ,
                          "number" : 42              ,
                          "boolean": True            ,
                          "null"   : None            ,
                          "array"  : [1, 2, 3]       ,
                          "object" : {"key": "value"}}

        self.source_json = {'a': self.json_data, 'b': self.json_data,
                            'c': self.json_data, 'd': self.json_data,
                            'e': self.json_data, 'f': self.json_data,
                            'g': self.json_data, 'h': self.json_data}

    def test__regression__call_1__load__simple_json(self):                                        # Test the top-level load operation
        with capture_duration() as duration:
            self.mgraph_json.load().from_data(self.source_json)                            # [FACT-1]
        #assert 0.5 < duration.seconds < 1                                      # BUG      # [FACT-2]
        assert 0    < duration.seconds < 0.2                                    # FIXED

        # FACTS:
        # FACT-1: MGraph__Json.load().from_json() is the entry point for JSON loading
        # FACT-2: Loading a moderately complex JSON (8 identical structures) takes > 0.5s

    def test__regression__call_2__load__from_data(self):                                          # Test MGraph__Json__Load.from_json
        loader = self.mgraph_json.load()
        with capture_duration() as duration:
            loader.from_data(self.source_json)                                              # [FACT-1]
        #assert 0.4 < duration.seconds < 0.8                                    # BUG       # [FACT-2]
        assert 0    < duration.seconds < 0.2                                    # FIXED

        # FACTS:
        # FACT-1: The performance issue exists in MGraph__Json__Load.from_json
        # FACT-2: Most of the total load time (~80%) is spent in from_json
        #
        # HYPOTHESIS:
        # HYP-1: The performance bottleneck is in the graph construction, not JSON parsing

    def test__regression__call_3__set_root_content(self):                                         # Test set_root_content operation
        graph = Domain__MGraph__Json__Graph()
        with capture_duration() as duration:                                                # [FACT-1]
            graph.set_root_content(self.source_json)
        #assert 0.4 < duration.seconds < 0.8                                                 # [FACT-2]
        assert 0    < duration.seconds < 0.2                                    # FIXED

        # FACTS:
        # FACT-1: set_root_content handles the initial graph structure creation
        # FACT-2: Almost all time from from_json is spent in set_root_content
        #
        # HYPOTHESIS:
        # HYP-1: The core performance issue is in the graph node/edge creation process

    def test__regression__call_4__new_dict_node(self):                                            # Test dictionary node creation
        graph = Domain__MGraph__Json__Graph()
        with capture_duration() as duration:                                                # [FACT-1][FACT-2]
            dict_node = graph.new_dict_node(self.source_json)
        #assert 0.4 < duration.seconds < 1                                      # BUG       # [FACT-3]
        assert 0    < duration.seconds < 0.2                                    # FIXED

        # FACTS:
        # FACT-1: new_dict_node creates the initial dictionary structure
        # FACT-2: This includes creating nodes for all properties recursively
        # FACT-3: Most time from set_root_content is in dict node creation
        #
        # HYPOTHESIS:
        # HYP-1: Property creation in dictionary nodes may be inefficient

    def test__regression__call_5__node_dict_update(self):                                         # Test dictionary update operation
        graph = Domain__MGraph__Json__Graph()
        dict_node = graph.new_dict_node()
        with capture_duration() as duration:                                                # [FACT-1]
            dict_node.update(self.source_json)
        #assert 0.4 < duration.seconds < 1                                      # BUG       # [FACT-2]
        assert 0 <= duration.seconds < 0.2                                    # FIXED

        # FACTS:
        # FACT-1: update() handles bulk property addition to dictionary nodes
        # FACT-2: Performance degrades similarly to new_dict_node
        #
        # HYPOTHESIS:
        # HYP-1: The issue may be in the property addition mechanism itself

    def test__regression__call_6__node_dict_add_property(self):                                   # Test single property addition
        graph = Domain__MGraph__Json__Graph()
        dict_node = graph.new_dict_node()
        with capture_duration() as duration:                                                # [FACT-1]
            dict_node.add_property('a', 42)                                                # [FACT-2]
        assert duration.seconds < 0.2                                                       # [FACT-3]

        # FACTS:
        # FACT-1: First property addition is fast
        # FACT-2: Simple values are handled efficiently
        # FACT-3: Initial property addition takes < 0.2s
        #
        # HYPOTHESIS:
        # HYP-1: Performance might degrade with number of existing properties

    def test__regression__call_7__add_property_linear_degradation(self):                         # Test property addition degradation
        graph             = Domain__MGraph__Json__Graph()
        dict_node         = graph.new_dict_node()
        previous_duration = 0

        with capture_duration() as total_duration:                                         # [FACT-1]
            for key, value in self.source_json.items():                                   # [FACT-2]
                with capture_duration() as partial_duration:
                    dict_node.add_property(key, value)
                if previous_duration:
                    assert partial_duration.seconds > previous_duration -0.10            # [FACT-3]
                previous_duration = partial_duration.seconds

        #assert 0.5 < total_duration.seconds < 1                                # BUG     # [FACT-4]
        assert 0.0  < total_duration.seconds < 0.2                              # FIXED

        with capture_duration() as duration:                                              # [FACT-5]
            edges = dict_node.models__from_edges()
            list(edges)
        assert duration.seconds < 0.2                                                     # [FACT-6]

        # FACTS:
        # FACT-1: Multiple property additions show performance degradation
        # FACT-2: Each property contains identical complex structure
        # FACT-3: Each subsequent add_property call takes longer
        # FACT-4: Total time for 8 properties is 0.5-1s
        # FACT-5: Edge traversal is performed in add_property
        # FACT-6: Direct edge traversal remains fast
        #
        # HYPOTHESIS:
        # HYP-1: Performance issue is in repeated edge scanning during property addition
        # HYP-2: Each property addition scans all existing edges

    def test__bug__check_for_property_section__in_add_property(self):
        #if in_github_action():
        pytest.skip("Legacy test that covered old bug and performance issue, see if see we still need it (this was not taking 25% of the test execution time)")

        class Bug__Domain__MGraph__Json__Node__Dict(Domain__MGraph__Json__Node__Dict):
            def add_property__update_existing(self, name: str, value: Any):                                       # the code below is the actual code from the add_property method (the first part)
                for edge in self.models__from_edges():
                    property_node = self.model__node_from_edge(edge)
                    if property_node.data.node_type == Schema__MGraph__Json__Node__Property:
                        if property_node.data.node_data.name == name:
                            for value_edge in self.graph.node__from_edges(property_node.node_id):

                                value_node = self.graph.node(value_edge.to_node_id())
                                if value_node.data.node_type is Schema__MGraph__Json__Node__Value:
                                    value_node.data.node_data.value = value
                                    return

            def add_property__add_node(self, name:str, value:Any):
                property_name__schema__node_data = Schema__MGraph__Json__Node__Property__Data(name      = name )
                property_name__schema__node      = Schema__MGraph__Json__Node__Property      (node_data = property_name__schema__node_data)
                property_name__model__node       = self.graph.add_node                       (node      = property_name__schema__node     )

            def add_property__add_node_and_edge(self, name:str, value:Any):
                property_name__schema__node_data  = Schema__MGraph__Json__Node__Property__Data(name      = name )
                property_name__schema__node       = Schema__MGraph__Json__Node__Property      (node_data = property_name__schema__node_data)
                property_name__model__node        = self.graph.add_node                       (node      = property_name__schema__node     )

                property_value__schema__node_data = Schema__MGraph__Json__Node__Value__Data  (value     = value, value_type=type(value)      )
                property_value__node_value        = Schema__MGraph__Json__Node__Value         (node_data = property_value__schema__node_data )
                property_value__model__node       = self.graph.add_node                       (node      = property_value__node_value        )

                #self.graph.new_edge(from_node_id=self.node_id                      , to_node_id=property_name__model__node.node_id )           # no need to add the edge to the base dict
                self.graph.new_edge(from_node_id=property_name__model__node.node_id, to_node_id=property_value__model__node.node_id)



        # Hypothesis 1
        an_bug_domain_node_1 = Bug__Domain__MGraph__Json__Node__Dict()                        # we are going to call the add_property without adding new nodes
        with capture_duration() as duration__without_adding_edges:
            with an_bug_domain_node_1 as _:
                for i in range(100):                                                            # adding 100 properties (this could be 10000, and would still be under 0.01 seconds)
                    _.add_property__update_existing('a', 42)
                    assert _.graph.nodes_ids() == []
                    assert _.graph.edges_ids() == []

        assert duration__without_adding_edges.seconds  < 0.002                              # the duration is under 0.002 seconds  which is what it should be (it is actually smaller but the duration.seconds precision is 0.001 secs)

        # Hypothesis 2
        an_bug_domain_node_2 = Bug__Domain__MGraph__Json__Node__Dict()
        total_duration__with_only_value_node__update_existing = 0
        total_duration__with_only_value_node__add_node        = 0
        with capture_duration() as duration__with_only_value_node:
            with an_bug_domain_node_2 as _:
                assert _.graph.nodes_ids() == []                                            # confirm there are no nodes here
                for i in range(1, 100):
                    with capture_duration() as duration__with_only_value_node__update_existing:
                        _.add_property__update_existing('a', 42)                    #
                    total_duration__with_only_value_node__update_existing += duration__with_only_value_node__update_existing.seconds

                    with capture_duration() as duration__with_only_value_node__add_node:
                        _.add_property__add_node       ('a', 42)                    # this will now add a node
                    total_duration__with_only_value_node__add_node += duration__with_only_value_node__add_node.seconds

                    assert len(_.graph.nodes_ids()) == i                                    # confirm the number of nodes is increased
                    assert _.graph.edges_ids() == []                                        # confirm no edges
        assert duration__with_only_value_node               .seconds < 0.040                # confirm we now have a performance impact
        assert total_duration__with_only_value_node__update_existing < 0.003                # but the update_existing still has good performance
        assert 0.0 <= total_duration__with_only_value_node__add_node < 0.030                # the extra duration was caused by the self.graph.add_node call

        # Hypothesis 3
        an_bug_domain_node_3 = Bug__Domain__MGraph__Json__Node__Dict()
        with capture_duration() as duration__with__node_and_edge:
            with an_bug_domain_node_3 as _:
                assert _.graph.nodes_ids() == []                                            # confirm there are no nodes here
                for i in range(1, 100):
                    _.add_property__update_existing  ('a', 42)

                    _.add_property__add_node_and_edge('a', 42)

        assert 0.20 < duration__with__node_and_edge.seconds < 0.80                          # confirm we now have a performance impact

        # Hypothesis 4
        an_bug_domain_node_4 = Bug__Domain__MGraph__Json__Node__Dict()
        total_duration__duration__with__node_and_edge__update_existing     = 0
        total_duration__duration__with__node_and_edge__add_node_and_edge   = 0
        previous__duration__duration__with__node_and_edge__update_existing = 0
        with capture_duration() as duration__with__node_and_edge:
            with an_bug_domain_node_4 as _:
                assert _.graph.nodes_ids() == []                                            # confirm there are no nodes here
                for i in range(1, 101):
                    with capture_duration() as duration__duration__with__node_and_edge__update_existing:
                        _.add_property__update_existing  ('a', 42)
                    total_duration__duration__with__node_and_edge__update_existing += duration__duration__with__node_and_edge__update_existing.seconds
                    if previous__duration__duration__with__node_and_edge__update_existing:
                        assert duration__duration__with__node_and_edge__update_existing.seconds + 0.006 > previous__duration__duration__with__node_and_edge__update_existing

                    previous__duration__duration__with__node_and_edge__update_existing = duration__duration__with__node_and_edge__update_existing.seconds

                    with capture_duration() as duration__duration__with__node_and_edge__add_node_and_edge:
                        _.add_property__add_node_and_edge('a', 42)
                    total_duration__duration__with__node_and_edge__add_node_and_edge+= duration__duration__with__node_and_edge__add_node_and_edge.seconds
                    assert len(_.graph.nodes_ids()) == i *2                                       # confirm the number of nodes is increased (by a factor of two, since have a new node for the property and one for the value)
                    assert len(_.graph.edges_ids()) == i                                          # confirm that the edges number is increasing

        assert len(_.graph.nodes_ids()) == 200                                                    # at the end we have 200 nodes
        assert len(_.graph.edges_ids()) == 100                                                    # and 100 edges

        assert 0.2   < duration__with__node_and_edge.seconds                              < 0.80     # confirm we now have a performance impact
        assert 0.2   < total_duration__duration__with__node_and_edge__update_existing     < 0.80     # confirm that the impact is on the update_existing code
        assert 0    <= total_duration__duration__with__node_and_edge__add_node_and_edge   < 0.11     # confirm that add_node_and_edge have just about no performance impact
        assert 0     < previous__duration__duration__with__node_and_edge__update_existing < 0.02     # confirm that the last call to add_property__update_existing took about 0.015 ms (which is a lot when this method is called 100s of times)




                    # @pytest.mark.skip("run only when needing a call trace")
    # @trace_calls(include=['mgraph_db'], show_duration=True, duration_padding=130, show_class=True)
    # def test__trace__performance__mgraph_json__load__from_json(self):
    #     mgraph_json = MGraph__Json()
    #     simple_json = {'a':42}
    #     mgraph_json.load().from_data(simple_json)