from unittest                                                               import TestCase
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Labels     import Schema__MGraph__Index__Data__Labels
from osbot_utils.helpers.performance.Performance_Measure__Session           import Performance_Measure__Session
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict       import Type_Safe__Dict


class test_Schema__MGraph__Index__Data__Labels(TestCase):                           # Test default values and types

    def test__defaults(self):                                                       # Test default attribute types and values
        with Schema__MGraph__Index__Data__Labels() as _:
            assert type(_.edges_predicates       ) is Type_Safe__Dict
            assert type(_.edges_by_predicate     ) is Type_Safe__Dict
            assert type(_.edges_incoming_labels  ) is Type_Safe__Dict
            assert type(_.edges_by_incoming_label) is Type_Safe__Dict
            assert type(_.edges_outgoing_labels  ) is Type_Safe__Dict
            assert type(_.edges_by_outgoing_label) is Type_Safe__Dict

            assert _.edges_predicates        == {}
            assert _.edges_by_predicate      == {}
            assert _.edges_incoming_labels   == {}
            assert _.edges_by_incoming_label == {}
            assert _.edges_outgoing_labels   == {}
            assert _.edges_by_outgoing_label == {}

    def test__json(self):                                                           # Test JSON serialization
        with Schema__MGraph__Index__Data__Labels() as _:
            json_data = _.json()
            assert json_data == { 'edges_predicates'       : {},
                                  'edges_by_predicate'     : {},
                                  'edges_incoming_labels'  : {},
                                  'edges_by_incoming_label': {},
                                  'edges_outgoing_labels'  : {},
                                  'edges_by_outgoing_label': {}}

    def test__object_creation_count(self):                                          # Count objects created during construction
        creation_count = {'value': 0}
        original_init  = Type_Safe.__init__

        def counting_init(self, **kwargs):
            creation_count['value'] += 1
            original_init(self, **kwargs)

        Type_Safe.__init__ = counting_init
        try:
            _ = Schema__MGraph__Index__Data__Labels()
            count = creation_count['value']
        finally:
            Type_Safe.__init__ = original_init

        assert count == 1                                                           # Only the schema itself (Dicts don't count as Type_Safe)

    def test__construction_time(self):                                              # Verify construction time is reasonable
        with Performance_Measure__Session() as _:
            _.measure(Schema__MGraph__Index__Data__Labels)

        construction_us = _.result.final_score / 1000
        assert construction_us <= 200