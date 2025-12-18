from unittest                                                                         import TestCase
from osbot_utils.utils.Objects                                                        import base_classes
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Graph
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Node
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Edge
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Display
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Edge__Renderer      import PlantUML__Edge__Renderer
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Base                import PlantUML__Base
from mgraph_db.providers.simple.MGraph__Simple                                        import MGraph__Simple


class test_PlantUML__Edge__Renderer(TestCase):

    @classmethod
    def setUpClass(cls):                                                              # shared test resources
        cls.config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

    def setUp(self):
        self.mgraph_simple = MGraph__Simple()

    def safe_id(self, node_id):                                                       # helper to sanitize node ID for PlantUML
        safe_str = str(node_id).replace('-', '_').replace(' ', '_')
        safe_str = ''.join(c if c.isalnum() or c == '_' else '_' for c in safe_str)
        if safe_str and safe_str[0].isdigit():
            safe_str = f'n_{safe_str}'
        return safe_str or 'node'

    def test__init__(self):                                                           # test auto-initialization
        with PlantUML__Edge__Renderer() as _:
            assert type(_)                  is PlantUML__Edge__Renderer
            assert PlantUML__Base           in base_classes(_)                        # inherits from base
            assert _.config                 is None
            assert _.graph                  is None
            assert _.index                  is None

    def test__init____with_config(self):                                              # test with config
        with PlantUML__Edge__Renderer(config=self.config) as _:
            assert _.config                 is self.config

    def test_render__basic(self):                                                     # test basic edge rendering
        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_from     = mgraph_data.node(from_node.node_id)
        domain_to       = mgraph_data.node(to_node.node_id)
        edge_data       = domain_edge.edge.data
        from_id_safe    = self.safe_id(from_node.node_id)
        to_id_safe      = self.safe_id(to_node.node_id)

        with PlantUML__Edge__Renderer(config=self.config) as _:
            result = _.render(domain_edge, domain_from, domain_to, edge_data)
            assert from_id_safe             in result                                 # sanitized from ID
            assert to_id_safe               in result                                 # sanitized to ID
            assert '-->'                    in result                                 # default arrow style
            assert result                   == f'{from_id_safe} --> {to_id_safe}'

    def test_render__arrow_style_dotted(self):                                        # test dotted arrow style
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge(style='..>')                          ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_from     = mgraph_data.node(from_node.node_id)
        domain_to       = mgraph_data.node(to_node.node_id)
        edge_data       = domain_edge.edge.data
        from_id_safe    = self.safe_id(from_node.node_id)
        to_id_safe      = self.safe_id(to_node.node_id)

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(domain_edge, domain_from, domain_to, edge_data)
            assert '..>'                    in result                                 # dotted arrow
            assert result                   == f'{from_id_safe} ..> {to_id_safe}'

    def test_render__arrow_style_simple(self):                                        # test simple arrow style
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge(style='->')                           ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_from     = mgraph_data.node(from_node.node_id)
        domain_to       = mgraph_data.node(to_node.node_id)
        edge_data       = domain_edge.edge.data
        from_id_safe    = self.safe_id(from_node.node_id)
        to_id_safe      = self.safe_id(to_node.node_id)

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(domain_edge, domain_from, domain_to, edge_data)
            assert '->'                     in result
            assert result                   == f'{from_id_safe} -> {to_id_safe}'

    def test_render__arrow_style_inheritance(self):                                   # test inheritance arrow style
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge(style='--|>')                         ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_from     = mgraph_data.node(from_node.node_id)
        domain_to       = mgraph_data.node(to_node.node_id)
        edge_data       = domain_edge.edge.data
        from_id_safe    = self.safe_id(from_node.node_id)
        to_id_safe      = self.safe_id(to_node.node_id)

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(domain_edge, domain_from, domain_to, edge_data)
            assert '--|>'                   in result
            assert result                   == f'{from_id_safe} --|> {to_id_safe}'

    def test_render__arrow_style_composition(self):                                   # test composition arrow style
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge(style='*--')                          ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_from     = mgraph_data.node(from_node.node_id)
        domain_to       = mgraph_data.node(to_node.node_id)
        edge_data       = domain_edge.edge.data
        from_id_safe    = self.safe_id(from_node.node_id)
        to_id_safe      = self.safe_id(to_node.node_id)

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(domain_edge, domain_from, domain_to, edge_data)
            assert '*--'                    in result
            assert result                   == f'{from_id_safe} *-- {to_id_safe}'

    def test_render__arrow_style_aggregation(self):                                   # test aggregation arrow style
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge(style='o--')                          ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_from     = mgraph_data.node(from_node.node_id)
        domain_to       = mgraph_data.node(to_node.node_id)
        edge_data       = domain_edge.edge.data
        from_id_safe    = self.safe_id(from_node.node_id)
        to_id_safe      = self.safe_id(to_node.node_id)

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(domain_edge, domain_from, domain_to, edge_data)
            assert 'o--'                    in result
            assert result                   == f'{from_id_safe} o-- {to_id_safe}'

    def test_render__show_edge_type(self):                                            # test showing edge type
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_edge_type=True)               )

        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_from     = mgraph_data.node(from_node.node_id)
        domain_to       = mgraph_data.node(to_node.node_id)
        edge_data       = domain_edge.edge.data
        from_id_safe    = self.safe_id(from_node.node_id)
        to_id_safe      = self.safe_id(to_node.node_id)

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(domain_edge, domain_from, domain_to, edge_data)
            assert '<<'                     in result                                 # type shown with stereotype
            assert ':'                      in result                                 # label separator
            assert result                   == f'{from_id_safe} --> {to_id_safe} : <<Edge>>'

    def test_render__hide_predicate(self):                                            # test hiding predicate (no predicate to hide for Simple)
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_edge_predicate=False)         )

        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_from     = mgraph_data.node(from_node.node_id)
        domain_to       = mgraph_data.node(to_node.node_id)
        edge_data       = domain_edge.edge.data
        from_id_safe    = self.safe_id(from_node.node_id)
        to_id_safe      = self.safe_id(to_node.node_id)

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(domain_edge, domain_from, domain_to, edge_data)
            assert ':'                      not in result                             # no label separator
            assert result                   == f'{from_id_safe} --> {to_id_safe}'

    def test_render__hide_predicate_and_edge_type(self):                              # test hiding both predicate and edge type
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_edge_predicate=False,
                                                show_edge_type=False)              )

        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_from     = mgraph_data.node(from_node.node_id)
        domain_to       = mgraph_data.node(to_node.node_id)
        edge_data       = domain_edge.edge.data
        from_id_safe    = self.safe_id(from_node.node_id)
        to_id_safe      = self.safe_id(to_node.node_id)

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(domain_edge, domain_from, domain_to, edge_data)
            assert ':'                      not in result
            assert '<<'                     not in result
            assert result                   == f'{from_id_safe} --> {to_id_safe}'

    def test_render__with_none_edge_data(self):                                       # test with None edge_data
        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_from     = mgraph_data.node(from_node.node_id)
        domain_to       = mgraph_data.node(to_node.node_id)
        from_id_safe    = self.safe_id(from_node.node_id)
        to_id_safe      = self.safe_id(to_node.node_id)

        with PlantUML__Edge__Renderer(config=self.config) as _:
            result = _.render(domain_edge, domain_from, domain_to, None)              # explicitly pass None
            assert result                   == f'{from_id_safe} --> {to_id_safe}'

    def test_build_label__no_predicate(self):                                         # test label without predicate
        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        edge_data       = domain_edge.edge.data

        with PlantUML__Edge__Renderer(config=self.config) as _:
            label = _.build_label(domain_edge, edge_data)
            assert label                    is None                                   # no label for Simple edges

    def test_build_label__predicate_display_disabled(self):                           # test label with predicate display disabled
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_edge_predicate=False,
                                                show_edge_type=False)              )

        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        edge_data       = domain_edge.edge.data

        with PlantUML__Edge__Renderer(config=config) as _:
            label = _.build_label(domain_edge, edge_data)
            assert label                    is None

    def test_build_label__edge_type_enabled(self):                                    # test label with edge type enabled
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_edge_predicate=False,
                                                show_edge_type=True)               )

        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        edge_data       = domain_edge.edge.data

        with PlantUML__Edge__Renderer(config=config) as _:
            label = _.build_label(domain_edge, edge_data)
            assert '<<Edge>>'               in label

    def test_extract_predicate__none(self):                                           # test no predicate
        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)

        with PlantUML__Edge__Renderer(config=self.config) as _:
            predicate = _.extract_predicate(domain_edge)
            assert predicate                is None                                   # Simple edges have no predicate

    # ═══════════════════════════════════════════════════════════════════════════════
    # Tests for multiple edges
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_render__multiple_edges_same_config(self):                                # test rendering multiple edges
        with self.mgraph_simple.edit() as edit:
            node_a = edit.new_node()
            node_b = edit.new_node()
            node_c = edit.new_node()
            edge1  = edit.new_edge(from_node_id=node_a.node_id, to_node_id=node_b.node_id)
            edge2  = edit.new_edge(from_node_id=node_b.node_id, to_node_id=node_c.node_id)
            edge3  = edit.new_edge(from_node_id=node_a.node_id, to_node_id=node_c.node_id)

        mgraph_data = self.mgraph_simple.data()
        node_a_safe = self.safe_id(node_a.node_id)
        node_b_safe = self.safe_id(node_b.node_id)
        node_c_safe = self.safe_id(node_c.node_id)

        with PlantUML__Edge__Renderer(config=self.config) as _:
            # Edge 1: A -> B
            domain_edge1 = mgraph_data.edge(edge1.edge_id)
            domain_from1 = mgraph_data.node(node_a.node_id)
            domain_to1   = mgraph_data.node(node_b.node_id)
            result1      = _.render(domain_edge1, domain_from1, domain_to1, None)
            assert result1                  == f'{node_a_safe} --> {node_b_safe}'

            # Edge 2: B -> C
            domain_edge2 = mgraph_data.edge(edge2.edge_id)
            domain_from2 = mgraph_data.node(node_b.node_id)
            domain_to2   = mgraph_data.node(node_c.node_id)
            result2      = _.render(domain_edge2, domain_from2, domain_to2, None)
            assert result2                  == f'{node_b_safe} --> {node_c_safe}'

            # Edge 3: A -> C
            domain_edge3 = mgraph_data.edge(edge3.edge_id)
            domain_from3 = mgraph_data.node(node_a.node_id)
            domain_to3   = mgraph_data.node(node_c.node_id)
            result3      = _.render(domain_edge3, domain_from3, domain_to3, None)
            assert result3                  == f'{node_a_safe} --> {node_c_safe}'

    def test_render__self_loop_edge(self):                                            # test edge pointing to same node
        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()
            edge = edit.new_edge(from_node_id=node.node_id, to_node_id=node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_node     = mgraph_data.node(node.node_id)
        node_id_safe    = self.safe_id(node.node_id)

        with PlantUML__Edge__Renderer(config=self.config) as _:
            result = _.render(domain_edge, domain_node, domain_node, None)
            assert result                   == f'{node_id_safe} --> {node_id_safe}'

    def test_render__with_show_edge_type_and_custom_arrow(self):                      # test combined options
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge(style='..>')                          ,
            display = PlantUML__Config__Display(show_edge_type=True)               )

        with self.mgraph_simple.edit() as edit:
            from_node = edit.new_node()
            to_node   = edit.new_node()
            edge      = edit.new_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)

        mgraph_data     = self.mgraph_simple.data()
        domain_edge     = mgraph_data.edge(edge.edge_id)
        domain_from     = mgraph_data.node(from_node.node_id)
        domain_to       = mgraph_data.node(to_node.node_id)
        from_id_safe    = self.safe_id(from_node.node_id)
        to_id_safe      = self.safe_id(to_node.node_id)

        with PlantUML__Edge__Renderer(config=config) as _:
            result = _.render(domain_edge, domain_from, domain_to, None)
            assert '..>'                    in result
            assert '<<Edge>>'               in result
            assert result                   == f'{from_id_safe} ..> {to_id_safe} : <<Edge>>'