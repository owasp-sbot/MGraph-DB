from typing                                                                     import Union, Dict, List, Optional, Any
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id               import Node_Id
from osbot_utils.utils.Dev                                                      import pprint
from mgraph_db.providers.json.actions.exporters.MGraph__Export__Json__Dot       import MGraph__Export__Json__Dot
from mgraph_db.providers.json.actions.exporters.MGraph__Export__Json__Mermaid   import MGraph__Export__Json__Mermaid
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Dict            import Model__MGraph__Json__Node__Dict
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__List            import Model__MGraph__Json__Node__List
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Value           import Model__MGraph__Json__Node__Value
from osbot_utils.utils.Files                                                    import file_save
from osbot_utils.utils.Json                                                     import json_dumps
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph                import Domain__MGraph__Json__Graph
from mgraph_db.mgraph.actions.MGraph__Export                                    import MGraph__Export
from mgraph_db.mgraph.index.MGraph__Index                                       import MGraph__Index

class MGraph__Json__Export(MGraph__Export):
    graph: Domain__MGraph__Json__Graph

    def process_value_node(self, node_id: Node_Id) -> Any:
        domain_node = self.graph.node(node_id)
        model_node  = domain_node.node
        if isinstance(model_node, Model__MGraph__Json__Node__Value):
            return model_node.value
        return None

    def process_dict_node(self, node_id: Node_Id, index: MGraph__Index) -> Dict[str, Any]:
        result = {}
        for edge_id in index.edges_ids__from__node_id(node_id):
            property_id = index.edges_to_nodes()[edge_id][1]
            property_node = self.graph.node(property_id)

            if property_node:
                if hasattr(property_node.node_data, 'name'):
                    property_name = property_node.node_data.name
                    value_edges  = index.edges_ids__from__node_id(property_id)
                    if value_edges:
                        value_node_id = index.edges_to_nodes()[value_edges[0]][1]
                        result[property_name] = self.process_node(value_node_id, index)
                    else:
                        result[property_name] = None
        return result

    def process_list_node(self, node_id: Node_Id, index: MGraph__Index) -> List[Any]:
        result = []
        for edge_id in index.edges_ids__from__node_id(node_id):
            item_id = index.edges_to_nodes()[edge_id][1]
            item_value = self.process_node(item_id, index)
            result.append(item_value)
        return result

    def process_node(self, node_id: Node_Id, index: MGraph__Index) -> Any:
        domain_node = self.graph.node(node_id)
        model_node  = domain_node.node
        if not domain_node:
            return None

        if   isinstance(model_node, Model__MGraph__Json__Node__Value): return self.process_value_node(node_id)
        elif isinstance(model_node, Model__MGraph__Json__Node__Dict ): return self.process_dict_node (node_id, index)
        elif isinstance(model_node, Model__MGraph__Json__Node__List ): return self.process_list_node (node_id, index)
        return None

    def to_dict(self) -> Union[Dict, List, Any]:
        root_content = self.graph.root_content()
        if not root_content:
            return None
        index = self.graph.index()
        return self.process_node(root_content.node_id, index)

    def to_string(self, indent: Optional[int] = None) -> str:
        data = self.to_dict()
        return json_dumps(data, indent=indent)

    def to_file(self, file_path: str, indent: Optional[int] = None) -> bool:
        file_contents = self.to_string(indent=indent)
        if file_contents:
            file_save(contents=file_contents, path=file_path)
            return True
        return False

    def to_dot(self):
        return MGraph__Export__Json__Dot(graph=self.graph)

    def to_mermaid(self) -> MGraph__Export__Json__Mermaid:
        return MGraph__Export__Json__Mermaid(graph=self.graph)

    def print__dict(self):
        pprint(self.to_dict())