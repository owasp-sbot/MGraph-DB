import pytest
from unittest                                                       import TestCase
from mgraph_db.mgraph.schemas.safe_str.Safe_Str__Graph__Path import Safe_Str__Graph__Path, SAFE_STR__GRAPH__PATH__MAX_LENGTH


class test_Safe_Str__Graph__Path(TestCase):

    def test_valid_paths(self):
        """Test valid path patterns."""
        valid_paths = [
            "html.body.div"                                         ,   # Basic dot notation
            "html.body.div.p[1]"                                    ,   # With index notation
            "node.path:html.body"                                   ,   # With namespace separator
            "config-setting.value"                                  ,   # With hyphens
            "Domain__Node__Person"                                  ,   # Python type names are valid
            "a"                                                     ,   # Single char
            ""                                                      ,   # Empty allowed
            "deeply.nested.path.with.many.levels[1].and[2].indices" ,   # Deep nesting
            "UPPER_case_MIX"                                        ,   # Mixed case
            "item[0]"                                               ,   # Index at start level
            "a.b.c.d.e.f.g.h.i.j"                                   ,   # Many levels
            "config:database:host"                                  ,   # Multiple colons
            "path[1][2][3]"                                         ,   # Multiple indices
            "my-kebab-case.path"                                    ,   # Kebab case
            "my_snake_case.path"                                    ,   # Snake case
        ]
        for path in valid_paths:
            result = Safe_Str__Graph__Path(path)
            assert str(result) == path, f"Path '{path}' should be valid"

    def test_invalid_paths(self):                                                               # Test invalid path patterns
        invalid_paths = {
            "path with spaces"          : "path_with_spaces"            ,   # Spaces become _
            "path/with/slashes"         : "path_with_slashes"           ,   # Forward slashes become _
            "path\\backslash"           : "path_backslash"              ,   # Backslashes become _
            "path<with>brackets"        : "path_with_brackets"          ,   # Angle brackets become _
            "path;semicolon"            : "path_semicolon"              ,   # Semicolons become _
            "path{braces}"              : "path_braces_"                ,   # Curly braces become _
            "path|pipe"                 : "path_pipe"                   ,   # Pipe becomes _
            "path&ampersand"            : "path_ampersand"              ,   # Ampersand becomes _
            "path*asterisk"             : "path_asterisk"               ,   # Asterisk becomes _
            "path?question"             : "path_question"               ,   # Question mark becomes _
            "path#hash"                 : "path_hash"                   ,   # Hash becomes _
            "path@at"                   : "path_at"                     ,   # At symbol becomes _
            "path!exclaim"              : "path_exclaim"                ,   # Exclamation becomes _
            "path$dollar"               : "path_dollar"                 ,   # Dollar becomes _
            "path%percent"              : "path_percent"                ,   # Percent becomes _
            "path^caret"                : "path_caret"                  ,   # Caret becomes _
            "path+plus"                 : "path_plus"                   ,   # Plus becomes _
            "path=equals"               : "path_equals"                 ,   # Equals becomes _
            "path`backtick"             : "path_backtick"               ,   # Backtick becomes _
            "path~tilde"                : "path_tilde"                  ,   # Tilde becomes _
            "path'quote"                : "path_quote"                  ,   # Single quote becomes _
            'path"doublequote'          : "path_doublequote"            ,   # Double quote becomes _
        }
        for invalid_path, fixed_path in invalid_paths.items():
            assert Safe_Str__Graph__Path(invalid_path) == fixed_path

    def test_max_length_exceeded(self):
        """Test that paths exceeding max length are rejected."""
        long_path = "a" * (SAFE_STR__GRAPH__PATH__MAX_LENGTH + 1)
        with pytest.raises(Exception):
            Safe_Str__Graph__Path(long_path)

    def test_max_length_exact(self):
        """Test that paths at exactly max length are accepted."""
        exact_path = "a" * SAFE_STR__GRAPH__PATH__MAX_LENGTH
        result = Safe_Str__Graph__Path(exact_path)
        assert len(str(result)) == SAFE_STR__GRAPH__PATH__MAX_LENGTH

    def test_whitespace_trimming(self):
        """Test that whitespace is trimmed from paths."""
        path_with_whitespace = "  html.body  "
        result = Safe_Str__Graph__Path(path_with_whitespace)
        assert str(result) == "html.body"

    def test_empty_path_allowed(self):
        """Test that empty paths are allowed."""
        empty_path = Safe_Str__Graph__Path("")
        assert str(empty_path) == ""

