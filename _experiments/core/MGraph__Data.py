from mgraph_db.mgraph.MGraph             import MGraph
from osbot_utils.type_safe.Type_Safe     import Type_Safe
from osbot_utils.helpers.Print_Table     import Print_Table


class MGraph__Data(Type_Safe):
    graph : MGraph

    def graph_data(self):
        nodes_data = self.nodes_data()
        edges_data = self.edges_data()
        graph_data = {'nodes': nodes_data, 'edges': edges_data}
        return graph_data

    def edges(self):
        return self.graph.edges().values()

    def edges_data(self):
        edges_data = []
        for edge in self.edges():
            edges_data.append(edge.json())
        return edges_data

    def nodes(self):
        return self.graph.nodes().values()

    def nodes_data(self):
        nodes_data = []
        for node in self.nodes():
            nodes_data.append(node.json())
        return nodes_data


    def nodes__by_id(self):
        by_key = {}
        for node in self.nodes():
            by_key[node.node_id] = node
        return by_key

    def nodes_ids(self):
        return list(self.graph.nodes().keys())

    def nodes_edges(self):
        nodes__edges = {}
        for node in self.nodes():
            nodes__edges[node.node_id] = []
        for edge in self.edges():
            from_key = edge.from_node_id
            if from_key in nodes__edges:                                        # todo: add a better way to handle this, which is a weird situation, look also at a better way to do this assigment
                nodes__edges[from_key].append(edge.to_node_id)
        for node_key, edges_keys in nodes__edges.items():
            nodes__edges[node_key] = sorted(edges_keys)
        return nodes__edges

    # def map_paths(self, key, paths, all_paths, nodes_edges):
    #     key_edges = nodes_edges[key]
    #     new_paths = []
    #
    #     for edge_key in key_edges:
    #         for path in paths:
    #             if edge_key in path:
    #                 if path not in all_paths:
    #                     all_paths.append(path)
    #             else:
    #                 new_path = [*path, edge_key]
    #                 new_paths.append(new_path)
    #                 self.map_paths(edge_key, new_paths, all_paths, nodes_edges)
    #                 if new_path not in all_paths:
    #                     all_paths.append(new_path)
        # if new_paths:
        #     return new_paths

            # for edge_key in key_edges:
            #     self.map_paths(edge_key, paths, nodes_edges)
        #return paths

    # def nodes__find_all_paths(self):
    #     key         = self.nodes__keys()[0]
    #     nodes_edges = self.nodes_edges()
    #     #for key in self.nodes__keys():
    #     all_paths = []
    #     paths = [[key]]
    #     self.map_paths(key, paths,all_paths,  nodes_edges)
    #     pprint(all_paths)

    def print(self):
        with Print_Table() as _:
            _.set_title(self.graph.config.graph__title)
            for node_key, edges_keys in self.nodes_edges().items():
                row = {'key': node_key,  'edges': edges_keys}
                _.add_data(row)
            _.set_order('key', 'edges')
            _.print()

    def print_adjacency_matrix(self):
        adjacency_matrix = self.nodes_edges__adjacency_matrix()
        node_keys        = sorted(self.nodes_ids())
        with Print_Table() as _:
            for row in adjacency_matrix:
                _.add_data(row)
            _.set_order('node_id', *node_keys)
            _.print()


    def node_edges__to_from(self):
        # Initialize a dictionary to hold the edges to and from for each node
        node_connections = { node_key: {'edges_to': [], 'edges_from': []} for node_key in self.nodes_edges().keys() }


        for node_key, edges_keys in self.nodes_edges().items():                 # Fill 'edges_to' and 'edges_from' for each node
            node_connections[node_key]['edges_from'].extend(edges_keys)         # 'edges_from' are the outgoing edges from 'node_key'

            for edge_key in edges_keys:                                         # 'edges_to' are the incoming edges to the nodes in 'edges_keys'
                if edge_key in node_connections:                                # Check if the edge_key represents a valid node
                    node_connections[edge_key]['edges_to'].append(node_key)

        return node_connections

    def nodes_edges__adjacency_matrix(self):
        nodes_edges = self.nodes_edges()                                                    # Retrieve the nodes and their edges
        node_keys = sorted(nodes_edges.keys())                                              # Get a sorted list of unique node keys
        node_indices = {node_key: index for index, node_key in enumerate(node_keys)}        # Create a mapping of node keys to their respective indices
        size = len(node_keys)                                                               # Initialize a square matrix with empty strings
        matrix = [['' for _ in range(size)] for _ in range(size)]

        for node_key, edges_keys in nodes_edges.items():                                    # Fill the matrix with 'X' if there is an edge between two nodes
            for edge_key in edges_keys:                                                     # Find the matrix positions based on node indices
                row_index = node_indices[node_key]
                col_index = node_indices[edge_key]
                matrix[row_index][col_index] = 'X'

        table_data = []
        for i, row in enumerate(matrix):
            row_data = {'node_id': node_keys[i]}
            row_data.update({node_keys[j]: row[j] for j in range(size)})
            table_data.append(row_data)
        return table_data

