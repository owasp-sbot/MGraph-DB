import importlib
from typing                                       import Type
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from mgraph_db.mgraph.actions.MGraph__Defaults    import MGraph__Defaults
from osbot_utils.type_safe.Type_Safe              import Type_Safe



class MGraph__Type__Resolver(Type_Safe):                                                    # Resolves optional type fields to actual types using defaults
    mgraph_defaults: MGraph__Defaults                                                       # Auto-instantiated with base defaults

    @cache_on_self
    def resolve_type(self, type_path: str) -> Type:                                        # Convert 'module.path.ClassName' string to actual Type
        module_path, class_name = type_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    def node_type           (self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.node_type
    def node_data_type      (self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.node_data_type
    def edge_type           (self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.edge_type
    def edge_data_type      (self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.edge_data_type
    def graph_type          (self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.graph_type
    def graph_data_type     (self, type_value: Type = None) -> Type: return type_value or self.mgraph_defaults.graph_data_type

    def node_domain_type    (self, type_value: Type = None) -> Type: return type_value or self.resolve_type(self.mgraph_defaults.node_domain_type)
    def edge_domain_type    (self, type_value: Type = None) -> Type: return type_value or self.resolve_type(self.mgraph_defaults.edge_domain_type)
    def node_model_type     (self, type_value: Type = None) -> Type:
        return type_value or self.resolve_type(self.mgraph_defaults.node_model_type)
    def edge_model_type     (self, type_value: Type = None) -> Type: return type_value or self.resolve_type(self.mgraph_defaults.edge_model_type)
