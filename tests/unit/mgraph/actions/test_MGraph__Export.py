from unittest                                       import TestCase
from xml.etree.ElementTree                          import fromstring
from mgraph_db.mgraph.MGraph                        import MGraph
from mgraph_db.mgraph.actions.MGraph__Export        import MGraph__Export
from mgraph_db.mgraph.utils.MGraph__Static__Graph   import MGraph__Static__Graph
from osbot_utils.testing.__                         import __
from osbot_utils.testing.__helpers                  import obj


class test_MGraph__Export(TestCase):

    @classmethod
    def setUpClass(cls) -> None:                                                                # Initialize test data
        cls.linear_graph   = MGraph__Static__Graph.create_linear()                             # Linear graph with 3 nodes
        cls.circular_graph = MGraph__Static__Graph.create_circular()                           # Circular graph with 3 nodes
        cls.star_graph     = MGraph__Static__Graph.create_star()                               # Star graph with 3 spokes
        cls.complete_graph = MGraph__Static__Graph.create_complete()                           # Complete graph with 3 nodes

    def test__init__(self):
        mgraph = MGraph()
        with mgraph.export() as _:
            assert type(_) is MGraph__Export
            assert _.obj() == __( graph       = mgraph.graph.obj())

    def test_to__mgraph_json(self):                                                           # Test full graph export
        empty_graph = MGraph()
        data        = empty_graph.export().to__mgraph_json()
        assert data      == empty_graph.graph.model.data.json()
        assert obj(data) == __(edges        = __()                          ,
                               graph_data   = None                          ,
                               graph_id     = empty_graph.data().graph_id() ,
                               graph_type   = None                          ,
                               nodes        = __()                          ,
                               schema_types = None)

    def test_to__json(self):                                                                  # Test minimal JSON export
        node_ids = self.linear_graph.node_ids
        edge_ids = self.linear_graph.edge_ids
        with self.linear_graph.graph.export() as _:
            assert _.to__json() == {'edges': { str(edge_ids[0]): { 'edge_id'     : str(edge_ids[0])           ,
                                                                   'edge_type'   : '@schema_mgraph_edge' ,
                                                                   'from_node_id': str(node_ids[0])           ,
                                                              'to_node_id'  : str(node_ids[1]) }          ,
                                               str(edge_ids[1]): { 'edge_id'     : str(edge_ids[1])           ,
                                                              'edge_type'   : '@schema_mgraph_edge' ,
                                                              'from_node_id': str(node_ids[1])           ,
                                                              'to_node_id'  : str(node_ids[2])}          },
                                    'graph_id': str(_.graph.graph_id())  ,
                                    'nodes'  : { str(node_ids[0]): { 'node_data': {}                     ,
                                                                'node_id'  : str(node_ids[0])            ,
                                                                'node_type': '@schema_mgraph_node'  },
                                                 str(node_ids[1]): { 'node_data': {}                     ,
                                                                'node_id'  : str(node_ids[1])            ,
                                                                'node_type': '@schema_mgraph_node'  },
                                                 str(node_ids[2]): { 'node_data': {}                     ,
                                                                'node_id'  : str(node_ids[2])            ,
                                                                'node_type': '@schema_mgraph_node'  }}}                          # Third node

    def test_to__xml(self):                                                                  # Test XML export
        with self.linear_graph.graph.export() as _:
            xml_str = _.to__xml()                                           # Get XML and parse it
            root    = fromstring(xml_str)

            assert root.tag == 'graph'                                      # Verify root structure
            nodes = root.find('nodes')
            edges = root.find('edges')
            assert nodes is not None
            assert edges is not None

            node_elements = nodes.findall('node')                           # Verify nodes
            assert len(node_elements) == len(self.linear_graph.node_ids)
            for node in node_elements:
                assert node.get('id') in self.linear_graph.node_ids

            edge_elements = edges.findall('edge')                           # Verify edges
            assert len(edge_elements) == len(self.linear_graph.edge_ids)
            for edge in edge_elements:
                assert edge.get('id') in self.linear_graph.edge_ids
                from_node = edge.find('from')
                to_node = edge.find('to')
                assert from_node is not None
                assert to_node is not None
                assert from_node.text in self.linear_graph.node_ids
                assert to_node.text in self.linear_graph.node_ids

            node_ids = self.linear_graph.node_ids                       # Verify XML string
            edge_ids = self.linear_graph.edge_ids
            assert xml_str == f"""\
<?xml version="1.0" encoding="UTF-8"?>
<graph>
  <nodes>
    <node id="{node_ids[0]}"/>
    <node id="{node_ids[1]}"/>
    <node id="{node_ids[2]}"/>
  </nodes>
  <edges>
    <edge id="{edge_ids[0]}">
      <from>{node_ids[0]}</from>
      <to>{node_ids[1]}</to>
    </edge>
    <edge id="{edge_ids[1]}">
      <from>{node_ids[1]}</from>
      <to>{node_ids[2]}</to>
    </edge>
  </edges>
</graph>"""

    def test_to__graphml(self):                                                             # Test GraphML export
        with self.linear_graph.graph.export() as _:
            xml_str = _.to__graphml()                                                       # Get XML and parse it
            root    = fromstring(xml_str)

            graphml_ns = 'http://graphml.graphdrawing.org/xmlns'                            # Verify root element and namespace
            graph      = root.find(f'{{{graphml_ns}}}graph')                                     # Need namespace for find/findall )
            nodes      = graph.findall(f'{{{graphml_ns}}}node')                                  # Verify nodes
            edges      = graph.findall(f'{{{graphml_ns}}}edge')
            node_ids   = set(node.get('id') for node in nodes)

            assert 'xmlns="http://graphml.graphdrawing.org/xmlns"' in xml_str  # Instead of checking the attribute directly, verify the namespace is in the raw XML

            assert root.tag                 == f'{{{graphml_ns}}}graphml'                                   # Namespace is included in tag
            assert graph                    is not None
            assert graph.get('id')          == 'G'
            assert graph.get('edgedefault') == 'directed'
            assert len(nodes)               == len(self.linear_graph.node_ids)
            assert sorted(node_ids)         == sorted(set(str(id) for id in self.linear_graph.node_ids))
            assert len(edges)               == len(self.linear_graph.edge_ids)
            for edge in edges:                                                                              # Verify edges
                assert edge.get('id') in (str(id) for id in self.linear_graph.edge_ids)
                assert edge.get('source') in (str(id) for id in self.linear_graph.node_ids)
                assert edge.get('target') in (str(id) for id in self.linear_graph.node_ids)

            node_ids = self.linear_graph.node_ids                                                           # Verify exact output structure
            edge_ids = self.linear_graph.edge_ids
            expected_xml = f'''\
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <graph id="G" edgedefault="directed">
    <node id="{node_ids[0]}"/>
    <node id="{node_ids[1]}"/>
    <node id="{node_ids[2]}"/>
    <edge id="{edge_ids[0]}" source="{node_ids[0]}" target="{node_ids[1]}"/>
    <edge id="{edge_ids[1]}" source="{node_ids[1]}" target="{node_ids[2]}"/>
  </graph>
</graphml>'''
            assert xml_str == expected_xml

    def test_to__gexf(self):                                                          # Test GEXF export
        with self.linear_graph.graph.export() as _:
            xml_str = _.to__gexf()                                                    # Get XML and parse it
            root = fromstring(xml_str)

            # Verify root element and namespace
            gexf_ns = 'http://www.gexf.net/1.2draft'
            assert root.tag == '{' + gexf_ns + '}gexf'                               # Namespace is included in tag
            assert root.get('version') == '1.2'                                      # Verify version attribute
            assert 'xmlns="http://www.gexf.net/1.2draft"' in xml_str                # Verify namespace in raw XML

            # Verify graph element
            graph = root.find('{' + gexf_ns + '}graph')
            assert graph is not None
            assert graph.get('defaultedgetype') == 'directed'

            # Verify nodes section
            nodes_elem = graph.find('{' + gexf_ns + '}nodes')
            assert nodes_elem is not None
            nodes = nodes_elem.findall('{' + gexf_ns + '}node')
            assert len(nodes) == len(self.linear_graph.node_ids)
            node_ids = set(node.get('id') for node in nodes)
            assert sorted(node_ids) == sorted(set(str(id) for id in self.linear_graph.node_ids))

            # Verify edges section
            edges_elem = graph.find('{' + gexf_ns + '}edges')
            assert edges_elem is not None
            edges = edges_elem.findall('{' + gexf_ns + '}edge')
            assert len(edges) == len(self.linear_graph.edge_ids)
            for edge in edges:
                assert edge.get('id') in (str(id) for id in self.linear_graph.edge_ids)
                assert edge.get('source') in (str(id) for id in self.linear_graph.node_ids)
                assert edge.get('target') in (str(id) for id in self.linear_graph.node_ids)

            # Verify exact output structure
            node_ids = self.linear_graph.node_ids
            edge_ids = self.linear_graph.edge_ids
            expected_xml = f'''\
<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
  <graph defaultedgetype="directed">
    <nodes>
      <node id="{node_ids[0]}"/>
      <node id="{node_ids[1]}"/>
      <node id="{node_ids[2]}"/>
    </nodes>
    <edges>
      <edge id="{edge_ids[0]}" source="{node_ids[0]}" target="{node_ids[1]}"/>
      <edge id="{edge_ids[1]}" source="{node_ids[1]}" target="{node_ids[2]}"/>
    </edges>
  </graph>
</gexf>'''
            assert xml_str == expected_xml

    def test_to__dot(self):                                                                  # Test DOT graph export
        with self.linear_graph.graph.export() as _:
            _.export_dot().config.render.label_show_var_name = True
            _.export_dot().show_edge__id()
            dot = _.to__dot()
            assert dot.startswith('digraph {')
            assert dot.endswith('}')
            for node_id in self.linear_graph.node_ids:
                assert f'"{node_id}"' in dot
            with self.linear_graph.graph.data() as data:
                for edge in data.edges():
                    assert f'"{edge.from_node_id()}" -> "{edge.to_node_id()}" [label="  edge_id = \'{edge.edge_id}\'"]' in dot


        node_ids = self.linear_graph.node_ids                                                # Verify expected structure using actual IDs
        edge_ids = self.linear_graph.edge_ids
        expected_dot = f'''\
digraph {{
  "{node_ids[0]}"
  "{node_ids[1]}"
  "{node_ids[2]}"
  "{node_ids[0]}" -> "{node_ids[1]}" [label="  edge_id = \'{edge_ids[0]}\'"]
  "{node_ids[1]}" -> "{node_ids[2]}" [label="  edge_id = \'{edge_ids[1]}\'"]
}}'''
        assert dot == expected_dot

    def test_to__turtle(self):                                                              # Test RDF/Turtle export
        with self.linear_graph.graph.export() as _:
            turtle = _.to__turtle()
            assert '@prefix mg: <http://mgraph.org/> .' in turtle
            for node_id in self.linear_graph.node_ids:
                assert f'mg:{node_id} a mg:Node .' in turtle
            with self.linear_graph.graph.data() as data:
                for edge in data.edges():
                    assert f'mg:{edge.edge_id} mg:from mg:{edge.from_node_id()} ;' in turtle
                    assert f'            mg:to   mg:{edge.to_node_id()} .' in turtle

        node_ids = self.linear_graph.node_ids                                           # Verify expected structure using actual IDs
        edge_ids = self.linear_graph.edge_ids
        expected_turtle = f'''\
@prefix mg: <http://mgraph.org/> .

mg:{node_ids[0]} a mg:Node .
mg:{node_ids[1]} a mg:Node .
mg:{node_ids[2]} a mg:Node .

mg:{edge_ids[0]} mg:from mg:{node_ids[0]} ;
            mg:to   mg:{node_ids[1]} .

mg:{edge_ids[1]} mg:from mg:{node_ids[1]} ;
            mg:to   mg:{node_ids[2]} .
'''
        assert turtle == expected_turtle

    def test_to__ntriples(self):                                                            # Test N-Triples export
        with self.linear_graph.graph.export() as _:
            ntriples = _.to__ntriples()
            for node_id in self.linear_graph.node_ids:
                assert f'<urn:{node_id}> <urn:exists> "true" .' in ntriples
            with self.linear_graph.graph.data() as data:
                for edge in data.edges():
                    assert f'<urn:{edge.edge_id}> <urn:from> <urn:{edge.from_node_id()}> .' in ntriples
                    assert f'<urn:{edge.edge_id}> <urn:to> <urn:{edge.to_node_id()}> .' in ntriples

        # Verify expected structure using actual IDs
        node_ids = self.linear_graph.node_ids
        edge_ids = self.linear_graph.edge_ids
        expected_ntriples = f'''\
<urn:{node_ids[0]}> <urn:exists> "true" .
<urn:{node_ids[1]}> <urn:exists> "true" .
<urn:{node_ids[2]}> <urn:exists> "true" .
<urn:{edge_ids[0]}> <urn:from> <urn:{node_ids[0]}> .
<urn:{edge_ids[0]}> <urn:to> <urn:{node_ids[1]}> .
<urn:{edge_ids[1]}> <urn:from> <urn:{node_ids[1]}> .
<urn:{edge_ids[1]}> <urn:to> <urn:{node_ids[2]}> .'''
        assert ntriples == expected_ntriples

    def test_to__tgf(self):                                                                # Test TGF export
        with self.linear_graph.graph.export() as _:
            tgf = _.to__tgf()

            # Split into nodes and edges sections
            nodes_section, edges_section = tgf.split('#')

            # Verify nodes
            nodes = [n.strip() for n in nodes_section.strip().split('\n')]
            for node_id in self.linear_graph.node_ids:
                assert str(node_id) in nodes

            # Verify edges
            edges = [e.strip() for e in edges_section.strip().split('\n')]
            with self.linear_graph.graph.data() as data:
                for edge in data.edges():
                    expected_edge = f'{edge.from_node_id()} {edge.to_node_id()} {edge.edge_id}'
                    assert expected_edge in edges

    def test_to__cypher(self):                                                             # Test Neo4j Cypher export
        with self.linear_graph.graph.export() as _:
            cypher = _.to__cypher()
            assert cypher.startswith('CREATE')

            # Verify nodes
            for i, node_id in enumerate(self.linear_graph.node_ids):
                if i == 0:
                    assert f'  (n{i}:Node {{id: \'{node_id}\'}})' in cypher
                else:
                    assert f', (n{i}:Node {{id: \'{node_id}\'}})' in cypher

            # Verify edges
            with self.linear_graph.graph.data() as data:
                for i, edge in enumerate(data.edges()):
                    from_idx = self.linear_graph.node_ids.index(edge.from_node_id())
                    to_idx = self.linear_graph.node_ids.index(edge.to_node_id())
                    assert f', (n{from_idx})-[r{i}:CONNECTS {{id: \'{edge.edge_id}\'}}]->(n{to_idx})' in cypher

    def test_to__csv(self):                                                                # Test CSV export
        with self.linear_graph.graph.export() as _:
            csv_files = _.to__csv()

            # Verify nodes.csv
            nodes_csv = csv_files['nodes.csv'].split('\n')
            assert nodes_csv[0] == 'node_id'                                               # Header
            for node_id in self.linear_graph.node_ids:
                assert str(node_id) in nodes_csv

            # Verify edges.csv
            edges_csv = csv_files['edges.csv'].split('\n')
            assert edges_csv[0] == 'edge_id,from_node_id,to_node_id'                      # Header
            with self.linear_graph.graph.data() as data:
                for edge in data.edges():
                    expected_row = f'{edge.edge_id},{edge.from_node_id()},{edge.to_node_id()}'
                    assert expected_row in edges_csv

    # def test_all_export_formats(self):                                                      # Test and generate documentation for all supported export formats  using a linear graph as the test case.
    #
    #     export_methods = [('to__mgraph_json', 'json'    ),
    #                        ('to__json'      , 'json'    ),
    #                        ('to__xml'       , 'xml'     ),
    #                        ('to__dot'       , 'dot'     ),
    #                        ('to__graphml'   , 'graphml' ),
    #                        ('to__turtle'    , 'turtle'  ),
    #                        ('to__ntriples'  , 'ntriples'),
    #                        ('to__gexf'      , 'gexf'    ),
    #                        ('to__tgf'       , 'tgf'     ),
    #                        ('to__cypher'    , 'cypher'  ),]
    #
    #     graph = MGraph__Static__Graph.create_linear(3)                                      # Create a linear graph with 4 nodes
    #
    #     with graph.graph.export() as exporter, Stdout() as stdout:                          # Capture output for export formats
    #         print("# MGraph Export Formats\n")
    #         print("Demonstration of export formats using a 3-node linear graph.\n")
    #
    #         for method_name, format_name in export_methods:
    #
    #             export_method = getattr(exporter, method_name)                          # Dynamically call export method
    #             export_result = export_method()
    #
    #             print(f"## {method_name}\n")                                        # Format and print result
    #             print(f"```{format_name}\n")
    #             if isinstance(export_result, dict):
    #                 pprint(export_result)
    #             else:
    #                 print(export_result)
    #             print("```\n")
    #                                                                                                 # todo: handle CSV export separately if needed
    #         csv_files = exporter.to__csv()
    #         print("## CSV Export\n")
    #         print('### nodes.csv\n')
    #         print("```")
    #         print(csv_files['nodes.csv'])
    #         print("```")
    #
    #         print('### edges.csv\n')
    #         print("```")
    #         print(csv_files['edges.csv'])
    #         print("```")
    #
    #
    #
    #     tmp_file = '/tmp/mgraph_export.md'                              # Save output to markdown file
    #     file_create(path=tmp_file, contents=stdout.value())