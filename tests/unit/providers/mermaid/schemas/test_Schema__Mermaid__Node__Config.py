import re
import pytest
from unittest                                                           import TestCase
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data    import Schema__Mermaid__Node__Data
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Shape   import Schema__Mermaid__Node__Shape



class test_Schema__Mermaid__Node__Data(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.node_data = Schema__Mermaid__Node__Data(
            markdown         = True                               ,
            node_shape      = Schema__Mermaid__Node__Shape.circle,
            show_label      = True                               ,
            wrap_with_quotes= True
        )

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.node_data) is Schema__Mermaid__Node__Data
        assert self.node_data.markdown           is True
        assert self.node_data.node_shape         == Schema__Mermaid__Node__Shape.circle
        assert self.node_data.show_label         is True
        assert self.node_data.wrap_with_quotes   is True

    def test_type_safety_validation(self):                                          # Tests type safety validations
        expected_error_1 = ("On Schema__Mermaid__Node__Data, invalid type for attribute 'markdown'. "
                            "Expected '<class 'bool'>' but got '<class 'str'>'")
        with pytest.raises(ValueError, match=re.escape(expected_error_1)):
            Schema__Mermaid__Node__Data(markdown         = "not-a-bool"                      ,
                                        node_shape      = Schema__Mermaid__Node__Shape.circle,
                                        show_label      = True                               ,
                                        wrap_with_quotes= True)

        expected_error_2 = "Invalid value 'not-a-shape' for enum Schema__Mermaid__Node__Shape"
        with pytest.raises(ValueError, match=re.escape(expected_error_2)):
            Schema__Mermaid__Node__Data(markdown         = True                ,
                                        node_shape      = "not-a-shape"       ,
                                        show_label      = True                ,
                                        wrap_with_quotes= True                )


