from unittest                                                           import TestCase
from osbot_utils.utils.Objects                                          import type_full_name
from osbot_utils.testing.__                                             import __
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Dict    import Model__MGraph__Json__Node__Dict
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict  import Schema__MGraph__Json__Node__Dict


class test_Model__MGraph__Json__Node__Dict(TestCase):

    def test_init(self):                                                                            # Test base JSON dict node model initialization
        with Model__MGraph__Json__Node__Dict(data=Schema__MGraph__Json__Node__Dict()) as _:          # Create base JSON dict node model
            assert _.obj() == __(data = __(node_data = __()     ,
                                           node_id    = _.node_id,
                                           node_type  = type_full_name(Schema__MGraph__Json__Node__Dict)))

