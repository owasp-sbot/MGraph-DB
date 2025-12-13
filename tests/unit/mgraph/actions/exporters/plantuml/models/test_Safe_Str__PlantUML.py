from unittest                                                                         import TestCase
from mgraph_db.mgraph.actions.exporters.plantuml.models.safe_str.Safe_Str__PlantUML   import Safe_Str__PlantUML
from osbot_utils.utils.Objects                                                        import base_classes
from osbot_utils.type_safe.primitives.core.Safe_Str                                   import Safe_Str

class test_Safe_Str__PlantUML(TestCase):

    def test__init__(self):                                                           # test basic initialization
        puml = Safe_Str__PlantUML('@startuml\n@enduml')
        assert type(puml)               is Safe_Str__PlantUML
        assert Safe_Str                 in base_classes(puml)

    def test_preserves_at_symbol(self):                                               # @ must be preserved for directives
        puml = Safe_Str__PlantUML('@startuml')
        assert '@startuml'              == puml
        assert puml.startswith('@')

    def test_preserves_newlines(self):                                                # \n must be preserved for line breaks
        puml = Safe_Str__PlantUML('@startuml\ncard "Test"\n@enduml')
        assert '\n'                     in puml
        lines = puml.split('\n')
        assert len(lines)               == 3

    def test_preserves_hash_colors(self):                                             # # must be preserved for colors
        puml = Safe_Str__PlantUML('card "Test" as n1 #LightBlue')
        assert '#LightBlue'             in puml

    def test_preserves_quotes(self):                                                  # " must be preserved for labels
        puml = Safe_Str__PlantUML('card "My Label" as n1')
        assert '"My Label"'             in puml

    def test_preserves_arrows(self):                                                  # --> and other arrows must work
        puml = Safe_Str__PlantUML('n1 --> n2 : label')
        assert '-->'                    in puml

        puml = Safe_Str__PlantUML('n1 ..> n2')
        assert '..>'                    in puml

    def test_preserves_stereotypes(self):                                             # <<type>> must be preserved
        puml = Safe_Str__PlantUML('card "<<Node>>\\nvalue" as n1')
        assert '<<Node>>'               in puml

    def test_preserves_colon_labels(self):                                            # : for edge labels
        puml = Safe_Str__PlantUML('n1 --> n2 : has_property')
        assert ': has_property'         in puml

    def test_complete_plantuml_diagram(self):                                         # full diagram test
        diagram = '''@startuml
skinparam backgroundColor transparent
skinparam shadowing false
left to right direction
title My Graph

card "<<Node>>\\nAlice" as n1 #LightBlue
card "<<Node>>\\nBob" as n2 #LightGreen

n1 --> n2 : knows
@enduml'''
        puml = Safe_Str__PlantUML(diagram)

        assert '@startuml'              in puml
        assert '@enduml'                in puml
        assert 'skinparam'              in puml
        assert '#LightBlue'             in puml
        assert '-->'                    in puml
        assert ': knows'                in puml

    def test_removes_control_characters(self):                                        # should remove only control chars
        puml = Safe_Str__PlantUML('@startuml\x00\x08@enduml')                          # null and backspace
        assert '\x00'                   not in puml
        assert '\x08'                   not in puml
        assert '@startuml'              in puml                                       # @ preserved
        assert '@enduml'                in puml

    def test_max_length(self):                                                        # verify max length setting
        assert Safe_Str__PlantUML.max_length == 1024 * 1024                           # 1MB

    def test_preserves_whitespace(self):                                              # whitespace preserved
        puml = Safe_Str__PlantUML('  card "Test" as n1  ')
        assert puml.startswith('  ')                                                  # leading spaces preserved
        assert puml.endswith('  ')                                                    # trailing spaces preserved