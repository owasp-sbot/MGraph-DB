from unittest                                                       import TestCase
from mgraph_db.mgraph.actions.MGraph__Defaults                      import MGraph__Defaults
from mgraph_db.mgraph.actions.MGraph__Type__Resolver                import MGraph__Type__Resolver
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value           import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                   import Domain__MGraph__Edge
from mgraph_db.mgraph.models.Model__MGraph__Node                    import Model__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Edge                    import Model__MGraph__Edge


class test_MGraph__Type__Resolver(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization of MGraph__Type__Resolver
        with MGraph__Type__Resolver() as _:
            assert type(_)                  is MGraph__Type__Resolver
            assert type(_.mgraph_defaults)  is MGraph__Defaults                             # Defaults auto-instantiated

    def test_resolver_returns_value_when_not_none(self):                                    # Explicit types should pass through unchanged
        with MGraph__Type__Resolver() as _:
            result = _.node_type(Schema__MGraph__Node)
            assert result is Schema__MGraph__Node                                           # Explicit value returned unchanged

    def test_resolver_returns_default_when_none(self):                                      # None should resolve to default
        with MGraph__Type__Resolver() as _:
            result = _.node_type(None)
            assert result is Schema__MGraph__Node                                           # Default used when None

    def test_resolver_all_methods_return_defaults_for_none(self):                           # All resolver methods should use defaults for None
        with MGraph__Type__Resolver() as _:
            # Schema types
            assert _.node_type      (None) is Schema__MGraph__Node
            assert _.edge_type      (None) is Schema__MGraph__Edge
            assert _.node_data_type (None) is _.mgraph_defaults.node_data_type
            assert _.edge_data_type (None) is _.mgraph_defaults.edge_data_type
            assert _.graph_type     (None) is _.mgraph_defaults.graph_type
            assert _.graph_data_type(None) is _.mgraph_defaults.graph_data_type

            # Domain types
            assert _.node_domain_type(None) is Domain__MGraph__Node
            assert _.edge_domain_type(None) is Domain__MGraph__Edge

            # Model types
            assert _.node_model_type(None) is Model__MGraph__Node
            assert _.edge_model_type(None) is Model__MGraph__Edge

    def test_resolver_uses_injected_defaults(self):                                         # Custom defaults should be used when injected
        class Custom__Defaults(MGraph__Defaults):
            node_type: type = Schema__MGraph__Node                                          # Override to base node

        custom_defaults = Custom__Defaults()
        resolver        = MGraph__Type__Resolver(mgraph_defaults=custom_defaults)

        result = resolver.node_type(None)
        assert result is Schema__MGraph__Node                                               # Custom default used

    def test_resolver_auto_instantiates_defaults(self):                                     # Resolver should auto-create MGraph__Defaults if not provided
        with MGraph__Type__Resolver() as _:
            assert _.mgraph_defaults is not None
            assert isinstance(_.mgraph_defaults, MGraph__Defaults)

    def test_resolver_explicit_takes_priority(self):                                        # Even with custom defaults, explicit values should take priority
        class Custom__Defaults(MGraph__Defaults):
            node_type: type = Schema__MGraph__Node

        resolver = MGraph__Type__Resolver(mgraph_defaults=Custom__Defaults())

        result = resolver.node_type(Schema__MGraph__Node__Value)                            # Pass explicit value
        assert result is Schema__MGraph__Node__Value                                        # Explicit value used, not custom default

    def test_resolver_consistency(self):                                                    # Resolver should be consistent across multiple calls
        with MGraph__Type__Resolver() as _:
            result1 = _.node_type(None)
            result2 = _.node_type(None)
            assert result1 is result2                                                       # Same result for same input

            result3 = _.edge_type(None)
            result4 = _.edge_type(None)
            assert result3 is result4                                                       # Consistent for edge types too

    def test_resolver_independence(self):                                                   # Different resolvers should be independent
        class Custom__Defaults__A(MGraph__Defaults):
            node_type: type = Schema__MGraph__Node

        class Custom__Defaults__B(MGraph__Defaults):
            node_type: type = Schema__MGraph__Node__Value

        resolver_a = MGraph__Type__Resolver(mgraph_defaults=Custom__Defaults__A())
        resolver_b = MGraph__Type__Resolver(mgraph_defaults=Custom__Defaults__B())

        assert resolver_a.node_type(None) is Schema__MGraph__Node                           # Resolver A uses its defaults
        assert resolver_b.node_type(None) is Schema__MGraph__Node__Value                    # Resolver B uses different defaults