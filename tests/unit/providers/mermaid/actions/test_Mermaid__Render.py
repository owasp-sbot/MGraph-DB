from unittest                                                               import TestCase
from osbot_utils.testing.Temp_File                                          import Temp_File
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id           import Safe_Id
from osbot_utils.utils.Files                                                import file_exists
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Edge               import Domain__Mermaid__Edge
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Node               import Domain__Mermaid__Node
from osbot_utils.testing.__                                                 import __
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Diagram_Direction import Schema__Mermaid__Diagram__Direction
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Diagram__Type     import Schema__Mermaid__Diagram__Type
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Shape       import Schema__Mermaid__Node__Shape
from mgraph_db.providers.mermaid.MGraph__Mermaid                            import MGraph__Mermaid
from osbot_utils.testing.Stdout                                             import Stdout
from osbot_utils.utils.Str                                                  import str_dedent

class test_Mermaid__Render(TestCase):

    def setUp(self):
        self.mermaid        = MGraph__Mermaid()
        self.mermaid_render = self.mermaid.render()
        self.mermaid_edit   = self.mermaid.edit()
        self.mermaid_data   = self.mermaid.data()

    def test__init__(self):
        with self.mermaid_render as _:
            expected_data = __(graph             = _.graph.obj(),
                               mermaid_code      = [])
            assert _              is not None
            assert _.obj()        == expected_data



    def test_code(self):
        expected_code = str_dedent("""
                                        flowchart TD
                                            A[Christmas] -->|Get money| B(Go shopping)
                                            B --> C{Let me think}
                                            C -->|One| D[Laptop]
                                            C -->|Two| E[iPhone]
                                            C -->|Three| F[fa:fa-car Car]
                                            """)


        with self.mermaid_edit as _:
            _.render_config().add_nodes         = False
            _.render_config().line_before_edges = False
            _.set_direction(Schema__Mermaid__Diagram__Direction.TD)
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.new_node(key=Safe_Id('A'), label='Christmas'    ).wrap_with_quotes(False).shape_default    ()
            _.new_node(key=Safe_Id('B'), label='Go shopping'  ).wrap_with_quotes(False).shape_round_edges()
            _.new_node(key=Safe_Id('C'), label='Let me think' ).wrap_with_quotes(False).shape_rhombus    ()
            _.new_node(key=Safe_Id('D'), label='Laptop'       ).wrap_with_quotes(False)
            _.new_node(key=Safe_Id('E'), label='iPhone'       ).wrap_with_quotes(False)
            _.new_node(key=Safe_Id('F'), label='fa:fa-car Car').wrap_with_quotes(False)
            _.add_edge('A', 'B', label='Get money').output_node_from().output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('B', 'C'                   ).output_node_to()
            _.add_edge('C', 'D', label='One'      ).output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('C', 'E', label='Two'      ).output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('C', 'F', label='Three'    ).output_node_to().edge_mode__lr_using_pipe()


        with self.mermaid_render as _:
            file_path = _.save()

            assert file_exists(file_path) is True

            assert _.code() == ( 'flowchart TD\n'
                                 '    A["A"] -->|Get money| B["B"]\n'
                                 '    B --> C["C"]\n'
                                 '    C -->|One| D["D"]\n'
                                 '    C -->|Two| E["E"]\n'
                                 '    C -->|Three| F["F"]')
            return
            assert expected_code          == _.code()

            with Stdout() as stdout:
                _.print_code()

            assert stdout.value() == expected_code + '\n'
            assert _.mermaid_code == expected_code.splitlines()

            _.reset_code()
            assert _.mermaid_code  == []
            assert expected_code   == _.code()
            assert _.mermaid_code  != []

    def test_code__more_cases(self):
        with self.mermaid_edit as _:
            _.add_directive('init: {"flowchart": {"htmlLabels": false}} ')
            # assert _.code() == ('%%{init: {"flowchart": {"htmlLabels": false}} }%%\n'
            #                     'graph LR\n')

            self.mermaid_render.code()
            _.new_node(key=Safe_Id('markdown'), label='This **is** _Markdown_').markdown()

            self.mermaid_render.code_create(recreate=True)

            #return

            assert self.mermaid_render.code() == ('%%{init: {"flowchart": {"htmlLabels": false}} }%%\n'
                                                  'graph LR\n'
                                                  '    markdown["`This **is** _Markdown_`"]\n')

            assert self.mermaid_render.render_config.diagram_type == Schema__Mermaid__Diagram__Type.graph

    def test_print_code(self):
        with self.mermaid_edit as _:
            _.add_edge(from_node_key=Safe_Id('from_node'), to_node_key=Safe_Id('to_node'))
        with self.mermaid_render as _:
            with Stdout() as stdout:
                _.print_code()
        assert stdout.value() == ('graph LR\n'
                                  '    from_node["from_node"]\n'
                                  '    to_node["to_node"]\n'
                                  '\n'
                                  '    from_node --> to_node\n')

    def test_render_edge(self):
        render_edge = self.mermaid_render.render_edge                               # helper method to make the code more readable
        with self.mermaid_edit as _:
            mermaid_edge = _.new_edge()
            from_node_id = mermaid_edge.from_node_id
            to_node_id   = mermaid_edge.to_node_id
            from_node    = self.mermaid_data.node(from_node_id)
            to_node      = self.mermaid_data.node(to_node_id  )

            assert type(mermaid_edge) is Domain__Mermaid__Edge
            assert self.mermaid_render.graph == _.graph                             # make sure these are the same
            assert type(from_node) is Domain__Mermaid__Node
            assert type(to_node) is Domain__Mermaid__Node
            assert render_edge(mermaid_edge) == f'    { from_node.key} --> {to_node.key}'

        with self.mermaid_edit as _:
            from_node.label = Safe_Id('from node')
            to_node  .label = Safe_Id('to node'  )
            assert render_edge(mermaid_edge) == f'    {from_node.key} --> {to_node.key}'
            mermaid_edge.label = 'link_type'

            assert render_edge(mermaid_edge) == f'    {from_node.key} --"{mermaid_edge.label}"--> {to_node.key}'
            mermaid_edge.edge_mode__lr_using_pipe()
            assert render_edge(mermaid_edge) == f'    {from_node.key} -->|{mermaid_edge.label}| {to_node.key}'
            mermaid_edge.output_node_to()
            assert render_edge(mermaid_edge) == f'    {from_node.key} -->|{mermaid_edge.label}| {to_node.key}["to_node"]'

    def test__render_node__node_shape(self):
        render_node = self.mermaid_render.render_node
        with self.mermaid_edit.new_node(key=Safe_Id('id')) as _:
            assert render_node(_                                                ) == '    id["id"]'
            assert render_node(_.shape(''                                      )) == '    id["id"]'
            assert render_node(_.shape('aaaaa'                                 )) == '    id["id"]'
            assert render_node(_.shape('round_edges'                           )) == '    id("id")'
            assert render_node(_.shape('rhombus'                               )) == '    id{"id"}'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.default    )) == '    id["id"]'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.rectangle  )) == '    id["id"]'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.round_edges)) == '    id("id")'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.rhombus    )) == '    id{"id"}'

    def test_save(self):
        with Temp_File() as temp_file:
            assert temp_file.delete()
            with self.mermaid_edit as _:
                _.add_node(key=Safe_Id('abc'))
                _.add_node(key=Safe_Id('xyz'))
                _.add_edge(Safe_Id('abc'), Safe_Id('xyz'))
            with self.mermaid_render as _:
                assert temp_file.exists() is False
                _.save(target_file=temp_file.path())
                assert temp_file.exists() is True
                assert _.code()           in temp_file.contents()
                assert _.code_markdown()  == temp_file.contents()



    def test__config__edge__output_node_from(self):
        with self.mermaid_edit as _:
            new_edge = _.add_edge(Safe_Id('id'), Safe_Id('id2')).output_node_from()

        with self.mermaid_render as _:
            assert _.code()                             == 'graph LR\n    id["id"]\n    id2["id2"]\n\n    id["id"] --> id2'
            assert new_edge.edge_config.output_node_from     is True
            assert _.render_edge(new_edge) == '    id["id"] --> id2'
            new_edge.output_node_from(False)
            assert new_edge.edge_config.output_node_from     is False
            assert _.render_edge(new_edge) == '    id --> id2'




# example = """
# flowchart TD
#     A[Christmas] -->|Get money| B(Go shopping)
#     B --> C{Let me think}
#     C -->|One| D[Laptop]
#     C -->|Two| E[iPhone]
#     C -->|Three| F[fa:fa-car Car]
#
# """
#             other_examples = """
# xychart-beta
#     title "Sales Revenue"
#     x-axis [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
#     y-axis "Revenue (in $)" 4000 --> 11000
#     bar [1000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
#     line [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
#
# mindmap
#   root((mindmap))
#     Origins
#
#       Long history
#       ::icon(fa fa-book)
#       Popularisation
#         British popular psychology author Tony Buzan
#     Research
#       On effectivness<br/>and features
#       On Automatic creation
#         Uses
#             Creative techniques
#             Strategic planning
#             Argument mapping
#     Tools
#       Pen and paper
#       Mermaid
# journey
#     title My working day
#     section Go to work
#       Make tea: 5: Me
#       Go upstairs: 3: Me
#       Do work: 1: Me, Cat
#     section Go home
#       Go downstairs: 5: Me
#       Sit down: 3: Me
# gantt
#     title A Gantt Diagram
#     dateFormat  YYYY-MM-DD
#     section Section
#     A task           :a1, 2014-01-01, 30d
#     Another task     :after a1  , 20d
#     section Another
#     Task in sec      :2014-01-12  , 12d
#     another task      : 24d
# erDiagram
#     CUSTOMER }|..|{ DELIVERY-ADDRESS : has
#     CUSTOMER ||--o{ ORDER : places
#     CUSTOMER ||--o{ INVOICE : "liable for"
#     DELIVERY-ADDRESS ||--o{ ORDER : receives
#     INVOICE ||--|{ ORDER : covers
#     ORDER ||--|{ ORDER-ITEM : includes
#     PRODUCT-CATEGORY ||--|{ PRODUCT : contains
#     PRODUCT ||--o{ ORDER-ITEM : "ordered in"
# stateDiagram-v2
#     [*] --> Still
#     Still --> [*]
#     Still --> Moving
#     Moving --> Still
#     Moving --> Crash
#     Crash --> [*]
# classDiagram
#     Animal <|-- Duck
#     Animal <|-- Fish
#     Animal <|-- Zebra
#     Animal : +int age
#     Animal : +String gender
#     Animal: +isMammal()
#     Animal: +mate()
#     class Duck{
#       +String beakColor
#       +swim()
#       +quack()
#     }
#     class Fish{
#       -int sizeInFeet
#       -canEat()
#     }
#     class Zebra{
#       +bool is_wild
#       +run()
#     }
# flowchart TD
#    A[Christmas] -->|Get money| B(Go shopping)
#    B --> C{Let me think}
#    C -->|One| D[Laptop]
#    C -->|Two| E[iPhone]
#    C -->|Three| F[fa:fa-car Car]
#
# gitGraph LR:
#    commit "Ashish"
#    branch newbranch
#    checkout newbranch
#    commit id:"1111"
#    commit tag:"test"
#    checkout main
#    commit type: HIGHLIGHT
#    commit
#    merge newbranch
#    commit
#    branch b2
#    commit tag:"b2 tag"
# sequenceDiagram
#    participant web as Web Browser
#    participant blog as Blog Service
#    participant account as Account Service
#    participant mail as Mail Service
#    participant db as Storage
#
#    Note over web,db: The user must be logged in to submit blog posts
#    web->>+account: Logs in using credentials
#    account->>db: Query stored accounts
#    db->>account: Respond with query result
#
#    alt Credentials not found
#        account->>web: Invalid credentials
#    else Credentials found
#        account->>-web: Successfully logged in
#
#        Note over web,db: When the user is authenticated, they can now submit new posts
#        web->>+blog: Submit new post
#        blog->>db: Store post data
#
#        par Notifications
#            blog--)mail: Send mail to blog subscribers
#            blog--)db: Store in-site notifications
#        and Response
#            blog-->>-web: Successfully posted
#        end
#    end
#
# sequenceDiagram
#     participant Alice
#     participant Bob
#     Alice->>John: Hello John, how are you?
#     loop Healthcheck
#         John->>John: Fight against hypochondria
#     end
#     Note right of John: Rational thoughts<br/>prevail...
#     John-->>Alice: Great!
#     John->>Bob: How about you?
#     Bob-->>John: Jolly good!
# sequenceDiagram
#     loop Daily query
#         Alice->>Bob: Hello Bob, how are you?
#         alt is sick
#             Bob->>Alice: Not so good :(
#         else is well
#             Bob->>Alice: Feeling fresh like a daisy
#         end
#
#         opt Extra response
#             Bob->>Alice: Thanks for asking
#         end
#     end
# graph TB
#    sq[Square shape] --> ci((Circle shape))
#
#    subgraph A
#        od>Odd shape]-- Two line<br/>edge comment --> ro
#        di{Diamond with <br/> line break} -.-> ro(Rounded<br>square<br>shape)
#        di==>ro2(Rounded square shape)
#    end
#
#    %% Notice that no text in shape are added here instead that is appended further down
#    e --> od3>Really long text with linebreak<br>in an Odd shape]
#
#    %% Comments after double percent signs
#    e((Inner / circle<br>and some odd <br>special characters)) --> f(,.?!+-*ز)
#
#    cyr[Cyrillic]-->cyr2((Circle shape Начало));
#
#     classDef green fill:#9f6,stroke:#333,stroke-width:2px;
#     classDef orange fill:#f96,stroke:#333,stroke-width:4px;
#     class sq,e green
#     class di orange
# pie title NETFLIX
#         "Time spent looking for movie" : 90
#         "Time spent watching it" : 10
# sequenceDiagram
#
#    Alice ->> Bob: Hello Bob, how are you?
#    Bob-->>John: How about you John?
#    Bob--x Alice: I am good thanks!
#    Bob-x John: I am good thanks!
#    Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.
#
#    Bob-->Alice: Checking with John...
#    Alice->John: Yes... John, how are you?
#
#
#     """

# graph TB
#     classDef bigText font-size:40px,background-color:blue, color:red,padding:1;
#     classDef smallText font-size:5px;
#
#     classDef green fill:#9f6,stroke:#333,stroke-width:2px;
#     classDef orange fill:#f96,stroke:#333,stroke-width:4px;
#
#
#     C["`A formatted text
#         ===========
#         .Emojis and
#         **bold** and
#         *italics*`"]
#
#     A[Node A]
#     B[Node B]
#
#     A --> B
#
#     class A bigText
#     class B smallText
#
#     class C orange
#
