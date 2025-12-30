import importlib
from typing                                       import Type
from mgraph_db.mgraph.actions.MGraph__Defaults    import MGraph__Defaults
from osbot_utils.type_safe.Type_Safe              import Type_Safe



class MGraph__Type__Resolver(Type_Safe):
    mgraph_defaults: MGraph__Defaults

    _node_model_type : type = None                                          # On-Demand-cached resolved types (None = not yet resolved)
    _edge_model_type : type = None
    _node_domain_type: type = None
    _edge_domain_type: type = None

    def resolve_type(self, type_path: str) -> Type:                         # No caching decorator - callers handle caching
        module_path, class_name = type_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    # Direct passthrough methods (no resolve_type, no caching needed)
    def node_type      (self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.node_type
    def node_data_type (self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.node_data_type
    def edge_type      (self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.edge_type
    def edge_data_type (self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.edge_data_type
    def graph_type     (self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.graph_type
    def graph_data_type(self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.graph_data_type

    # On-Demand-cached resolve_type methods
    def node_model_type(self, type_value: Type = None) -> Type:
        if type_value is not None:
            return type_value
        if self._node_model_type is None:
            self._node_model_type = self.resolve_type(self.mgraph_defaults.node_model_type)
        return self._node_model_type

    def edge_model_type(self, type_value: Type = None) -> Type:
        if type_value is not None:
            return type_value
        if self._edge_model_type is None:
            self._edge_model_type = self.resolve_type(self.mgraph_defaults.edge_model_type)
        return self._edge_model_type

    def node_domain_type(self, type_value: Type = None) -> Type:
        if type_value is not None:
            return type_value
        if self._node_domain_type is None:
            self._node_domain_type = self.resolve_type(self.mgraph_defaults.node_domain_type)
        return self._node_domain_type

    def edge_domain_type(self, type_value: Type = None) -> Type:
        if type_value is not None:
            return type_value
        if self._edge_domain_type is None:
            self._edge_domain_type = self.resolve_type(self.mgraph_defaults.edge_domain_type)
        return self._edge_domain_type
