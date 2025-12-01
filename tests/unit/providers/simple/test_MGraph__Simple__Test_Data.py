from unittest                                             import TestCase
from osbot_utils.utils.Files                              import file_exists, file_delete
from mgraph_db.mgraph.MGraph                              import MGraph
from mgraph_db.providers.simple.MGraph__Simple            import MGraph__Simple
from osbot_utils.type_safe.Type_Safe                      import Type_Safe
from osbot_utils.utils.Objects                            import base_types
from mgraph_db.providers.simple.MGraph__Simple__Test_Data import MGraph__Simple__Test_Data


class test_MGraph__Simple__Test_Data(TestCase):

    def setUp(self):
        self.test_data = MGraph__Simple__Test_Data().create()

    def test_create(self):
        with self.test_data as _:
            assert _.data().nodes_ids() == _.nodes_ids()
            assert _.data().edges_ids() == _.edges_ids()
            assert type(_)              is MGraph__Simple__Test_Data
            assert base_types(_)        == [MGraph__Simple, MGraph, Type_Safe, object]

    def test__export__to_json(self):
        with self.test_data.data() as _:
            nodes_ids = _.nodes_ids()
            edges_ids = _.edges_ids()
        with self.test_data.export() as _:
            assert _.to__json() == {'edges'   : { edges_ids[0]: { 'edge_data'   : {}                    ,
                                                                  'edge_id'     : edges_ids[0]          ,
                                                                  'edge_label'  : None                  ,
                                                                  'edge_path'   : None                  ,   # NEW: path field
                                                                  'edge_type'   : '@schema_mgraph_edge' ,
                                                                  'from_node_id': nodes_ids[0]          ,
                                                                  'to_node_id'  : nodes_ids[1]          },
                                                  edges_ids[1]: { 'edge_data'   : {}                    ,
                                                                  'edge_id'     : edges_ids[1]          ,
                                                                  'edge_label'  : None                  ,
                                                                  'edge_path'   : None                  ,   # NEW: path field
                                                                  'edge_type'   : '@schema_mgraph_edge' ,
                                                                  'from_node_id': nodes_ids[0]          ,
                                                                  'to_node_id'  : nodes_ids[2]          }},
                                    'graph_id': _.graph.graph_id()                                      ,
                                    'graph_path': None                                                  ,
                                    'nodes'   : { nodes_ids[0]: { 'node_data': {'name': 'Node 1', 'value': 'A'},
                                                                  'node_id'  : nodes_ids[0]             ,
                                                                  'node_path': None                     ,   # NEW: path field
                                                                  'node_type': '@schema_simple_node'    },
                                                  nodes_ids[1]: { 'node_data': {'name': 'Node 2', 'value': 'B'},
                                                                  'node_id'  : nodes_ids[1]             ,
                                                                  'node_path': None                     ,   # NEW: path field
                                                                  'node_type': '@schema_simple_node'    },
                                                  nodes_ids[2]: { 'node_data': {'name': 'Node 3', 'value': 'C'},
                                                                  'node_id'  : nodes_ids[2]             ,
                                                                  'node_path': None                     ,   # NEW: path field
                                                                  'node_type': '@schema_simple_node'    }}}

    def test__export__to_dot(self):
        with self.test_data.data() as _:
            nodes_ids = _.nodes_ids()
            edges_ids = _.edges_ids()
        with self.test_data.export() as _:
            _.export_dot().config.render.label_show_var_name = True
            _.export_dot().show_node__value().show_edge__id()

            expected_dot = f"""digraph {{
  "{nodes_ids[0]}" [label="node_value='A'"]
  "{nodes_ids[1]}" [label="node_value='B'"]
  "{nodes_ids[2]}" [label="node_value='C'"]
  "{nodes_ids[0]}" -> "{nodes_ids[1]}" [label="  edge_id = '{edges_ids[0]}\'"]
  "{nodes_ids[0]}" -> "{nodes_ids[2]}" [label="  edge_id = '{edges_ids[1]}\'"]
}}"""
            assert _.to__dot() == expected_dot


    def test__export__to_mermaid(self):
        with self.test_data.data() as _:
            nodes_ids = _.nodes_ids()
            edges_ids = _.edges_ids()
        with self.test_data.export() as _:
            expected_mermaid = f"""\
graph TD
    {nodes_ids[0]}["value:A|name:Node 1"]
    {nodes_ids[1]}["value:B|name:Node 2"]
    {nodes_ids[2]}["value:C|name:Node 3"]
    {nodes_ids[0]} -->|{edges_ids[0]}| {nodes_ids[1]}
    {nodes_ids[0]} -->|{edges_ids[1]}| {nodes_ids[2]}"""

            assert _.to__mermaid() == expected_mermaid

    def test__export__to_mermaid__markdown(self):
        with self.test_data.export() as _:
            target_file = './mgraph-simple.md'
            dot_text    = _.to__mermaid()
            md_text     = _.to__mermaid__markdown(target_file)
            assert file_exists(target_file) is True
            assert dot_text in md_text
            assert file_delete(target_file)

    def test__index__stats(self):
        with self.test_data.index() as _:
            assert _.stats() == {'index_data': {'edge_to_nodes': 2,
                                                'edges_by_path': {},
                                                'edges_by_type': {'Schema__MGraph__Edge': 2},
                                                'node_edge_connections': {'avg_incoming_edges': 1,
                                                                          'avg_outgoing_edges': 1,
                                                                          'max_incoming_edges': 1,
                                                                          'max_outgoing_edges': 2,
                                                                          'total_nodes': 3},
                                                'nodes_by_path': {},
                                                'nodes_by_type': {'Schema__Simple__Node': 3}},
                                 'paths': {'edge_paths': {}, 'node_paths': {}},
                                 'summary': {'edges_with_paths': 0,
                                             'nodes_with_paths': 0,
                                             'total_edges': 2,
                                             'total_nodes': 3,
                                             'total_predicates': 0,
                                             'unique_edge_paths': 0,
                                             'unique_node_paths': 0}} != {'index_data': {'edge_to_nodes': 2,
                                                'edges_by_path': {},
                                                'edges_by_type': {'Schema__MGraph__Edge': 2},
                                                'node_edge_connections': {'avg_incoming_edges': 1,
                                                                          'avg_outgoing_edges': 1,
                                                                          'max_incoming_edges': 1,
                                                                          'max_outgoing_edges': 2,
                                                                          'total_nodes': 3},
                                                'nodes_by_path': {},
                                                'nodes_by_type': {'Schema__Simple__Node': 3}}}



