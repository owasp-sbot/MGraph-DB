from contextlib                                 import contextmanager
from unittest.mock                              import patch
from mgraph_db.utils.testing.MGraph__Test__Ids  import MGraph__Test__Ids

test_ids = MGraph__Test__Ids()

@contextmanager
def mgraph_test_ids():              # Context manager for deterministic sequential ID generation in tests
    test_ids.reset()

    from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id

    original_new = Obj_Id.__new__

    def patched_new(cls, *args, **kwargs):
        return str.__new__(cls, test_ids.next_id_from_context())

    with patch.object(Obj_Id, '__new__', patched_new):
        yield test_ids