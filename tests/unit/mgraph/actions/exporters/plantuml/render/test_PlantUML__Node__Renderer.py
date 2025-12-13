from unittest                                                                         import TestCase
from osbot_utils.utils.Objects                                                        import base_classes
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id       import Safe_Str__Id
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Graph
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Node
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Edge
from mgraph_db.mgraph.actions.exporters.plantuml.models.PlantUML__Config              import PlantUML__Config__Display
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Node__Renderer      import PlantUML__Node__Renderer
from mgraph_db.mgraph.actions.exporters.plantuml.render.PlantUML__Base                import PlantUML__Base
from mgraph_db.providers.simple.MGraph__Simple                                        import MGraph__Simple


class test_PlantUML__Node__Renderer(TestCase):

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
        with PlantUML__Node__Renderer() as _:
            assert type(_)                  is PlantUML__Node__Renderer
            assert PlantUML__Base           in base_classes(_)                        # inherits from base
            assert _.config                 is None
            assert _.graph                  is None
            assert _.index                  is None

    def test__init____with_config(self):                                              # test with config
        with PlantUML__Node__Renderer(config=self.config) as _:
            assert _.config                 is self.config

    def test_render__basic(self):                                                     # test basic node rendering
        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_safe  = self.safe_id(node.node_id)

        with PlantUML__Node__Renderer(config=self.config) as _:
            result = _.render(domain_node, node_data)
            assert 'card'                   in result                                 # default shape
            assert node_id_safe             in result                                 # sanitized ID
            assert '<<Simple__Node>>'               in result                                 # type name shown
            assert result                   == f'card "<<Simple__Node>>" as {node_id_safe}'

    def test_render__with_shape_rectangle(self):                                      # test rectangle shape
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(shape='rectangle')                    ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_safe  = self.safe_id(node.node_id)

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(domain_node, node_data)
            assert result.startswith('rectangle')                                     # rectangle shape
            assert result                   == f'rectangle "<<Simple__Node>>" as {node_id_safe}'

    def test_render__with_shape_component(self):                                      # test component shape
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(shape='component')                    ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_safe  = self.safe_id(node.node_id)

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(domain_node, node_data)
            assert result                   == f'component "<<Simple__Node>>" as {node_id_safe}'

    def test_render__with_shape_database(self):                                       # test database shape
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(shape='database')                     ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_safe  = self.safe_id(node.node_id)

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(domain_node, node_data)
            assert result                   == f'database "<<Simple__Node>>" as {node_id_safe}'

    def test_render__with_shape_cloud(self):                                          # test cloud shape
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(shape='cloud')                        ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_safe  = self.safe_id(node.node_id)

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(domain_node, node_data)
            assert result                   == f'cloud "<<Simple__Node>>" as {node_id_safe}'

    def test_render__with_default_color(self):                                        # test default color
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(default_color=Safe_Str__Id('LightBlue')),
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_safe  = self.safe_id(node.node_id)

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(domain_node, node_data)
            assert '#LightBlue'             in result                                 # color applied
            assert result                   == f'card "<<Simple__Node>>" as {node_id_safe} #LightBlue'

    def test_render__with_type_color_mapping(self):                                   # test type-specific color
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(
                        type_colors = {'Simple__Node': Safe_Str__Id('LightGreen')})        ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_safe  = self.safe_id(node.node_id)

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(domain_node, node_data)
            assert '#LightGreen'            in result                                 # color applied
            assert result                   == f'card "<<Simple__Node>>" as {node_id_safe} #LightGreen'

    def test_render__hide_type(self):                                                 # test hiding type
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_node_type=False)              )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_safe  = self.safe_id(node.node_id)

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(domain_node, node_data)
            assert '<<'                     not in result                             # type not shown
            assert result                   == f'card "Simple__Node" as {node_id_safe}'

    def test_render__show_id(self):                                                   # test showing node ID
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_node_id=True)                 )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_safe  = self.safe_id(node.node_id)
        node_id_short = str(node.node_id)[:8]

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(domain_node, node_data)
            assert f'[{node_id_short}'      in result                                 # truncated ID shown
            assert result                   == f'card "<<Simple__Node>>\\n[{node_id_short}]" as {node_id_safe}'

    def test_render__show_id_and_hide_type(self):                                     # test showing ID and hiding type
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_node_id=True, show_node_type=False))

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_safe  = self.safe_id(node.node_id)
        node_id_short = str(node.node_id)[:8]

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(domain_node, node_data)
            assert '<<'                     not in result
            assert f'[{node_id_short}'      in result
            assert result                   == f'card "[{node_id_short}]" as {node_id_safe}'

    def test_render__with_none_node_data(self):                                       # test with None node_data
        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_id_safe  = self.safe_id(node.node_id)

        with PlantUML__Node__Renderer(config=self.config) as _:
            result = _.render(domain_node, None)                                      # explicitly pass None
            assert 'card'                   in result
            assert node_id_safe             in result
            assert result                   == f'card "<<Simple__Node>>" as {node_id_safe}'

    def test_build_label__type_only(self):                                            # test label with type only
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_node_type  = True ,
                                                show_node_value = False)           )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data

        with PlantUML__Node__Renderer(config=config) as _:
            label = _.build_label(domain_node, node_data)
            assert '<<Simple__Node>>'               in label
            assert label                    == '<<Simple__Node>>'

    def test_build_label__nothing_shown(self):                                        # test label when nothing shown
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_node_type  = False,
                                                show_node_value = False,
                                                show_node_id    = False)           )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data

        with PlantUML__Node__Renderer(config=config) as _:
            label = _.build_label(domain_node, node_data)
            assert label                    == 'Simple__Node'                                 # fallback to type name

    def test_build_label__with_id(self):                                              # test label with ID
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node   ()                                  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(show_node_type  = True ,
                                                show_node_value = False,
                                                show_node_id    = True )           )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_short = str(node.node_id)[:8]

        with PlantUML__Node__Renderer(config=config) as _:
            label = _.build_label(domain_node, node_data)
            assert '<<Simple__Node>>'               in label
            assert f'[{node_id_short}'      in label
            assert label                    == f'<<Simple__Node>>\\n[{node_id_short}]'

    def test_resolve_color__no_mapping(self):                                         # test color without mapping
        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)

        with PlantUML__Node__Renderer(config=self.config) as _:
            color = _.resolve_color(domain_node)
            assert color                    is None                                   # no default color

    def test_resolve_color__with_default(self):                                       # test default color
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(default_color=Safe_Str__Id('white'))  ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)

        with PlantUML__Node__Renderer(config=config) as _:
            color = _.resolve_color(domain_node)
            assert color                    == 'white'

    def test_resolve_color__type_mapping_takes_precedence(self):                      # test type mapping precedence
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(
                        default_color = Safe_Str__Id('white')                      ,
                        type_colors   = {'Simple__Node': Safe_Str__Id('yellow')})          ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display()                                  )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)

        with PlantUML__Node__Renderer(config=config) as _:
            color = _.resolve_color(domain_node)
            assert color                    == 'yellow'                               # type mapping takes precedence

    def test_extract_value__none_data(self):                                          # test None node_data
        with PlantUML__Node__Renderer(config=self.config) as _:
            value = _.extract_value(None)
            assert value                    is None

    def test_extract_value__with_node_data(self):                                     # test extract_value with real node_data
        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data

        with PlantUML__Node__Renderer(config=self.config) as _:
            value = _.extract_value(node_data)
            assert value                    is None                                   # Simple nodes don't have value attr

    # ═══════════════════════════════════════════════════════════════════════════════
    # Tests for multiple nodes
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_render__multiple_nodes_same_config(self):                                # test rendering multiple nodes
        with self.mgraph_simple.edit() as edit:
            node1 = edit.new_node()
            node2 = edit.new_node()
            node3 = edit.new_node()

        mgraph_data = self.mgraph_simple.data()

        with PlantUML__Node__Renderer(config=self.config) as _:
            results = []
            for node_id in [node1.node_id, node2.node_id, node3.node_id]:
                domain_node = mgraph_data.node(node_id)
                node_data   = domain_node.node_data
                result      = _.render(domain_node, node_data)
                results.append(result)
                node_id_safe = self.safe_id(node_id)
                assert result               == f'card "<<Simple__Node>>" as {node_id_safe}'

            assert len(results)             == 3
            assert len(set(results))        == 3                                      # all unique (different IDs)

    def test_render__with_all_options(self):                                          # test with all display options enabled
        config = PlantUML__Config(
            graph   = PlantUML__Config__Graph  ()                                  ,
            node    = PlantUML__Config__Node(
                        shape         = 'rectangle'                                ,
                        default_color = Safe_Str__Id('LightYellow'))               ,
            edge    = PlantUML__Config__Edge   ()                                  ,
            display = PlantUML__Config__Display(
                        show_node_type  = True                                     ,
                        show_node_value = True                                     ,
                        show_node_id    = True)                                    )

        with self.mgraph_simple.edit() as edit:
            node = edit.new_node()

        mgraph_data   = self.mgraph_simple.data()
        domain_node   = mgraph_data.node(node.node_id)
        node_data     = domain_node.node_data
        node_id_safe  = self.safe_id(node.node_id)
        node_id_short = str(node.node_id)[:8]

        with PlantUML__Node__Renderer(config=config) as _:
            result = _.render(domain_node, node_data)
            assert 'rectangle'              in result
            assert '<<Simple__Node>>'               in result
            assert f'[{node_id_short}'      in result
            assert '#LightYellow'           in result
            assert result                   == f'rectangle "<<Simple__Node>>\\n[{node_id_short}]" as {node_id_safe} #LightYellow'