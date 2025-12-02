from mgraph_db.mgraph.actions.MGraph__Type__Resolver                            import MGraph__Type__Resolver
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config  import MGraph__Export__Dot__Config
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                              import Domain__MGraph__Graph
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe


class MGraph__Export__Dot__Base(Type_Safe):
    config  : MGraph__Export__Dot__Config                                                   # Configuration for DOT export
    graph   : Domain__MGraph__Graph                                                         # Graph being exported
    resolver: MGraph__Type__Resolver                                                        # Auto-instantiated - provides type resolution

    def type_name__from__type(self, target_type: type) -> str:                              # create a nice value to show when we have a type
        if target_type:
            return target_type.__name__.split('__').pop().lower()
        return None