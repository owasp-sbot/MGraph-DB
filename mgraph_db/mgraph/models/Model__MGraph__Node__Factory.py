"""Factory for creating graph nodes with cached type resolution.

    Separates node creation logic into discrete steps for clarity:
    1. Determine if complete spec provided (fast path)
    2. Resolve node_type and node_data_type
    3. Split kwargs between node and node_data
    4. Create node_data object
    5. Create and add node to graph
    """

from typing                                                                 import Dict, Tuple, Any, TYPE_CHECKING
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id           import Node_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                    import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data             import Schema__MGraph__Node__Value__Data
from mgraph_db.mgraph.models.Model__MGraph__Graph                           import Model__MGraph__Graph
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Cache import type_safe_cache


class Model__MGraph__Node__Factory(Type_Safe):

    graph                   : Model__MGraph__Graph      = None                              # Parent graph reference
    _type_annotations_cache : Dict[type, Dict]                                              # Cache: node_type -> annotations
    _data_type_cache        : Dict[type, type]                                              # Cache: node_type -> node_data_type



    # --- Main Entry Point ---

    def create_node(self, **kwargs):                                                        # Main entry point - routes to appropriate creation method
        if self._has_complete_node_spec(kwargs):
            return self._create_from_complete_spec(kwargs)
        return self._create_with_type_resolution(kwargs)

    # --- Fast Path (complete spec provided) ---

    def _has_complete_node_spec(self, kwargs: Dict) -> bool:                                # Check if both node_type and node_data provided
        return 'node_type' in kwargs and 'node_data' in kwargs

    def _create_from_complete_spec(self, kwargs: Dict):                                     # Fast path when node_type and node_data are both provided
        node_type = kwargs.get('node_type')
        node_data = kwargs.get('node_data')
        del kwargs['node_data']
        node = node_type(node_data=node_data, **kwargs)
        return self.graph.add_node(node)

    # --- Type Resolution Path ---

    def _create_with_type_resolution(self, kwargs: Dict):                                   # Full path with type resolution
        node_type, node_data_type, add_node_type = self._resolve_node_types(kwargs)
        node_kwargs, data_kwargs                 = self._split_kwargs(kwargs, node_type, node_data_type)
        node_data                                = self._create_node_data(node_data_type, data_kwargs)
        node                                     = node_type(node_data=node_data, **node_kwargs)

        if add_node_type:                                                                   # Set node_type if not using defaults
            node.node_type = node_type

        return self.graph.add_node(node)

    def _resolve_node_types(self, kwargs: Dict) -> Tuple[type, type, bool]:                 # Returns (node_type, node_data_type, add_node_type_to_node)
        add_node_type_to_node = False

        if 'node_type' in kwargs:                                                           # Case 1: node_type provided in kwargs
            node_type      = kwargs.get('node_type')
            node_data_type = self._get_node_data_type_from_annotations(node_type)

        elif self.graph.data.schema_types is not None:                                      # Case 2: schema_types defined on graph
            node_type      = self.graph.data.schema_types.node_type
            node_data_type = self.graph.data.schema_types.node_data_type
            node_type      = self.graph.resolver.node_type(node_type)                       # Resolve if None
            node_data_type = self.graph.resolver.node_data_type(node_data_type)             # Resolve if None
            add_node_type_to_node = True

        elif self.graph.model_types.node_model_type:                                        # Case 3: model_types defined
            node_type      = self.graph.model_types.node_model_type.__annotations__.get('data')
            node_data_type = self._get_node_data_type_from_annotations(node_type)
            add_node_type_to_node = True

        else:                                                                               # Case 4: Fallback to defaults
            node_type      = self.graph.resolver.node_type(None)
            node_data_type = self.graph.resolver.node_data_type(None)

        return node_type, node_data_type, add_node_type_to_node

    def _get_node_data_type_from_annotations(self, node_type: type) -> type:                # Get node_data_type from node_type's annotations (with caching)
        annotations = self._get_type_annotations(node_type)
        return annotations.get('node_data')

    def _get_type_annotations(self, node_type: type) -> Dict:                               # Cached annotation lookup
        if node_type not in self._type_annotations_cache:
            self._type_annotations_cache[node_type] = dict(type_safe_cache.get_class_annotations(node_type))
        return self._type_annotations_cache[node_type]

    # --- Kwargs Processing ---

    def _split_kwargs(self, kwargs: Dict, node_type: type, node_data_type: type) -> Tuple[Dict, Dict]:  # Separate kwargs for node_type and node_data_type
        node_type_annotations      = self._get_type_annotations(node_type)
        node_data_type_annotations = self._get_type_annotations(node_data_type)

        node_kwargs = {}
        data_kwargs = {}

        for key, value in kwargs.items():                                                   # Split kwargs based on which class accepts them
            if key in node_type_annotations:
                node_kwargs[key] = value
            if key in node_data_type_annotations:
                data_kwargs[key] = value

        return node_kwargs, data_kwargs

    # --- Node Data Creation ---

    def _create_node_data(self, node_data_type: type, kwargs: Dict):                        # Create node_data object, handling special cases
        if node_data_type is Schema__MGraph__Node__Data:                                    # Schema__MGraph__Node__Data has no attributes
            return None

        if issubclass(node_data_type, Schema__MGraph__Node__Value__Data):                   # Handle value nodes that need unique key
            if kwargs == {}:
                kwargs['key'] = Node_Id(Node_Id(Obj_Id()))                                  # Ensure uniqueness for indexing

        return node_data_type(**kwargs)

    # --- Cache Management ---

    def clear_caches(self):                                                                 # Clear all caches (useful for testing)
        self._type_annotations_cache.clear()
        self._data_type_cache.clear()
        return self

    def cache_stats(self) -> Dict[str, int]:                                                # Return cache statistics
        return dict(type_annotations_cached = len(self._type_annotations_cache),
                    data_types_cached       = len(self._data_type_cache       ))