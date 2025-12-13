from unittest                                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Base                  import PlantUML__Base
from osbot_utils.utils.Objects                                                          import base_classes
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id         import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label      import Safe_Str__Label


class test_PlantUML__Base(TestCase):

    def test__init__(self):                                                           # test auto-initialization
        with PlantUML__Base() as _:
            assert type(_)                  is PlantUML__Base
            assert base_classes(_)          == [Type_Safe, object]
            assert _.graph                  is None                                   # no graph by default
            assert _.index                  is None                                   # no index by default

    def test_safe_id(self):                                                           # test ID sanitization
        with PlantUML__Base() as _:
            assert _.safe_id('abc-123')     == 'abc_123'                              # hyphens replaced
            assert _.safe_id('hello world') == 'hello_world'                          # spaces replaced
            assert _.safe_id('a!b@c#d')     == 'a_b_c_d'                              # special chars replaced
            assert type(_.safe_id('test'))  is Safe_Str__Id                           # returns Safe_Str__Id

    def test_safe_id__starts_with_number(self):                                       # test number prefix handling
        with PlantUML__Base() as _:
            assert _.safe_id('123abc')      == 'n_123abc'                             # prefixed with n_
            assert _.safe_id('42')          == 'n_42'                                 # pure number prefixed

    def test_safe_id__none_handling(self):                                            # test None input
        with PlantUML__Base() as _:
            assert _.safe_id(None)          == 'node'                                 # default value

    def test_safe_id__empty_handling(self):                                           # test empty input
        with PlantUML__Base() as _:
            assert _.safe_id('')            == 'node'                                 # default for empty

    def test_wrap_text(self):                                                         # test text wrapping
        with PlantUML__Base() as _:
            short_text = 'hello world'
            assert _.wrap_text(short_text, 40) == 'hello world'                       # no wrap needed

    def test_wrap_text__long_text(self):                                              # test wrapping at width
        with PlantUML__Base() as _:
            long_text = 'this is a very long text that should be wrapped'
            wrapped   = _.wrap_text(long_text, 20)
            assert '\\n' in wrapped                                                   # contains PlantUML newline

    def test_wrap_text__exact_width(self):                                            # test boundary condition
        with PlantUML__Base() as _:
            text = 'exactly forty characters in this text!!!'
            assert len(text) == 40
            assert _.wrap_text(text, 40)    == text                                   # no wrap at exact width

    def test_wrap_text__none_handling(self):                                          # test None input
        with PlantUML__Base() as _:
            assert _.wrap_text(None, 40)    == ''                                     # empty for None

    def test_wrap_text__empty_handling(self):                                         # test empty input
        with PlantUML__Base() as _:
            assert _.wrap_text('', 40)      == ''                                     # empty stays empty

    def test_type_name__from__type(self):                                             # test type name extraction
        with PlantUML__Base() as _:
            class Schema__MGraph__Node__Value: pass
            class Schema__Custom__Thing: pass
            class Plain__Class: pass

            result1 = _.type_name__from__type(Schema__MGraph__Node__Value)
            result2 = _.type_name__from__type(Schema__Custom__Thing)
            result3 = _.type_name__from__type(Plain__Class)

            assert result1                  == 'Node__Value'                          # prefix removed
            assert result2                  == 'Custom__Thing'                        # Schema__ removed
            assert result3                  == 'Plain__Class'                         # no matching prefix
            assert type(result1)            is Safe_Str__Label                        # returns Safe_Str__Label

    def test_type_name__from__type__none(self):                                       # test None type
        with PlantUML__Base() as _:
            assert _.type_name__from__type(None) == 'Node'                            # default value

    def test_escape_label(self):                                                      # test label escaping
        with PlantUML__Base() as _:
            assert _.escape_label('hello')          == 'hello'                        # no escaping needed
            assert _.escape_label('say "hi"')       == 'say \\"hi\\"'                 # quotes escaped
            assert _.escape_label("line1\nline2")   == 'line1\\nline2'                # newlines escaped
            assert _.escape_label("has\rcarriage")  == 'hascarriage'                  # carriage return removed

    def test_escape_label__none_handling(self):                                       # test None input
        with PlantUML__Base() as _:
            assert _.escape_label(None)     == ''                                     # empty for None

    def test_escape_label__empty_handling(self):                                      # test empty input
        with PlantUML__Base() as _:
            assert _.escape_label('')       == ''                                     # empty stays empty
