from unittest                                                                   import TestCase

import pytest

from mgraph_db.providers.graph_rag.actions.Graph_RAG__Document__Processor       import Graph_RAG__Document__Processor, DEFAULT__OPEN_AI__MODEL
from osbot_utils.helpers.xml.rss.RSS__Item                                      import RSS__Item
from osbot_utils.utils.Env                                                      import load_dotenv


class test_Graph_RAG__Document__Processor(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()

    def setUp(self):                                                                             # Initialize test environment
        self.api_llm   = API__LLM__Open()
        self.processor = Graph_RAG__Document__Processor(api_llm=self.api_llm)                   # Create processor instance
        self.sample_rss_item             = RSS__Item()                                          # Create sample RSS item
        self.sample_rss_item.title       = "Test Article"
        self.sample_rss_item.description = "Test content about technology"
        self.sample_rss_item.pubDate     = "2024-01-29"
        self.sample_rss_item.link        = "https://test.com/article"
        self.sample_rss_item.guid        = "2ff98947-e431-52c6-a851-60c01d2bbef8"
        self.sample_rss_item.categories  = ["tech", "news"]
        self.sample_rss_item.creator     = "Test Author"

    @pytest.mark.skip("test needs refactoring due to use of tools instead of functions")
    def test_create_entities_prompt(self):                                                      # Test prompt creation
        text   = "Sample text for entity extraction"
        prompt = self.processor.create_entities_prompt(text)

        assert type(prompt)                    is dict                                          # Verify prompt structure
        assert prompt['model']                 == DEFAULT__OPEN_AI__MODEL
        assert prompt['response_format']['type'] == "json_object"
        assert len(prompt['messages'])         == 2
        assert 'functions'                     in prompt
        assert len(prompt['functions'])        == 1

    # def test_create_entity(self):                                                              # Test entity creation
    #     entity_data = {
    #         "name": "TestEntity",
    #         "primary_domains": ["Testing", "Development"],
    #         "functional_roles": ["Test Framework"],
    #         "direct_relationships": [
    #             {"entity": "OtherEntity", "relationship_type": "uses", "strength": 0.8}
    #         ],
    #         "domain_relationships": [
    #             {"concept": "Software Testing", "relationship_type": "part_of",
    #              "category": "Process", "strength": 0.9}
    #         ],
    #         "ecosystem": {
    #             "platform": "TestPlatform",
    #             "standards": ["TestStandard"]
    #         },
    #         "confidence": 0.95
    #     }
    #
    #     entity = self.processor.create_entity(entity_data)
    #
    #     assert type(entity)                         is Schema__Graph_RAG__Entity                # Verify entity properties
    #     assert entity.node_data.name                == "TestEntity"
    #     assert len(entity.node_data.primary_domains) == 2
    #     assert entity.node_data.confidence          == 0.95
    #     assert "platform"                           in entity.node_data.ecosystem
    #
    # def test_extract_entities(self):                                                          # Test entity extraction
    #     sample_text = "cyber-news-1"                                                          # Using cached test data
    #     entities    = self.processor.extract_entities(sample_text)                            # Test extraction
    #
    #     assert len(entities)                     == 4                                         # Verify we got 4 entities
    #     assert type(entities[0])                 is Schema__Graph_RAG__Entity                # Check types
    #     assert type(entities[1])                 is Schema__Graph_RAG__Entity
    #     assert type(entities[2])                 is Schema__Graph_RAG__Entity
    #     assert type(entities[3])                 is Schema__Graph_RAG__Entity
    #
    #     # Verify specific entities from the cached response
    #     entity_names = [e.node_data.name for e in entities]
    #     assert "BuildFlow"              in entity_names                                       # Check specific entities
    #     assert "Continuous Integration" in entity_names
    #     assert "Machine Learning"       in entity_names
    #     assert "Development Team"       in entity_names
    #
    #     # Check structure of first entity
    #     buildflow = next(e for e in entities if e.node_data.name == "BuildFlow")
    #     assert len(buildflow.node_data.primary_domains)      == 2                            # Check data structure
    #     assert len(buildflow.node_data.functional_roles)     == 2
    #     assert len(buildflow.node_data.direct_relationships) == 3
    #     assert buildflow.node_data.confidence                > 0.9

    # def test_create_relations_prompt(self):                                                  # Test relation prompt creation
    #     entity_data_1 = Schema__Graph_RAG__Entity__Data(name="Entity1")
    #     entity_data_2 = Schema__Graph_RAG__Entity__Data(name="Entity2")
    #     entities = [ Schema__Graph_RAG__Entity(node_data=entity_data_1),
    #                  Schema__Graph_RAG__Entity(node_data=entity_data_2) ]
    #
    #     text = "Test text for relations"
    #
    #     prompt = self.processor.create_relations_prompt(entities, text)                      # Create prompt
    #
    #     assert type(prompt)            is str                                                # Verify prompt content
    #     assert "Entity1"               in prompt
    #     assert "Entity2"               in prompt
    #     assert "relation_type"         in prompt
    #     assert "confidence"            in prompt

    # def test_create_relation(self):                                                         # Test relation creation
    #     entity_data_1 = Schema__Graph_RAG__Entity__Data(name="Source")
    #     entity_data_2 = Schema__Graph_RAG__Entity__Data(name="Target")
    #     entities = [ Schema__Graph_RAG__Entity(node_data=entity_data_1),
    #                  Schema__Graph_RAG__Entity(node_data=entity_data_2) ]
    #
    #
    #     relation_data = {
    #         "source": "Source",
    #         "target": "Target",
    #         "relation_type": "USES",
    #         "confidence": 0.9,
    #         "context": "Test context"
    #     }
    #
    #     relation = self.processor.create_relation(relation_data, entities)                  # Create relation
    #
    #     assert type(relation)                       is Schema__Graph_RAG__Relation          # Verify properties
    #     assert relation.edge_data.relation_type     == "USES"
    #     assert relation.edge_data.confidence        == 0.9
    #     assert relation.edge_data.context           == "Test context"
    #     assert relation.from_node_id                == entities[0].node_id
    #     assert relation.to_node_id                  == entities[1].node_id

    # def test_valid_relation(self):                                                         # Test relation validation
    #     entity_data_1 = Schema__Graph_RAG__Entity__Data(name="Entity1")
    #     entity_data_2 = Schema__Graph_RAG__Entity__Data(name="Entity2")
    #     entities = [ Schema__Graph_RAG__Entity(node_data=entity_data_1),
    #                  Schema__Graph_RAG__Entity(node_data=entity_data_2) ]
    #
    #     valid_relation = {                                                                 # Test valid case
    #         "source": "Entity1",
    #         "target": "Entity2"
    #     }
    #     assert self.processor.valid_relation(valid_relation, entities) is True
    #
    #     invalid_relation = {                                                              # Test invalid case
    #         "source": "NonExistent1",
    #         "target": "NonExistent2"
    #     }
    #     assert self.processor.valid_relation(invalid_relation, entities) is False