# MGraph-DB PlantUML Export Engine

PlantUML exporter for MGraph-DB following the DOT exporter architecture pattern.

## Target Location in MGraph-DB

```
mgraph_db/mgraph/actions/exporters/plantuml/
├── __init__.py
├── MGraph__Export__PlantUML.py          # Main orchestrator
├── models/
│   ├── __init__.py
│   └── PlantUML__Config.py              # Type_Safe config objects
└── render/
    ├── __init__.py
    ├── PlantUML__Base.py                # Base renderer class
    ├── PlantUML__Node__Renderer.py      # Node → statement
    ├── PlantUML__Edge__Renderer.py      # Edge → statement
    └── PlantUML__Format__Generator.py   # @startuml/@enduml + directives
```

## Architecture

Mirrors the DOT exporter four-layer pattern:

| Layer | Class | Responsibility |
|-------|-------|----------------|
| Orchestrator | `MGraph__Export__PlantUML` | Owns config, renderers, context; assembles output |
| Config | `PlantUML__Config*` | Type_Safe configuration objects |
| Renderers | `PlantUML__*__Renderer` | Convert nodes/edges to statements |
| Format | `PlantUML__Format__Generator` | Emit @startuml, directives, @enduml |

## Key Design Decisions

### Complete Statements (Not Fragments)

DOT emits attribute fragments. PlantUML emits **complete statements**:

```python
# DOT (fragments)
attrs = ['shape=box', 'color=blue']
line = f'{node_id} [{", ".join(attrs)}]'

# PlantUML (complete statements)
line = f'rectangle "Label" as {node_id} #LightBlue'
```

### Callbacks Preserved

```python
exporter = MGraph__Export__PlantUML(graph=graph, data=data, index=index)

# Custom node rendering
def my_node_callback(node, node_data):
    if is_special(node):
        return f'actor "Special" as {node.node_id()}'
    return None  # use default

exporter.on_add_node = my_node_callback
```

### Type_Safe Throughout

- NO raw `str`, `int`, `float` for domain concepts
- NO docstrings (inline comments only)
- Vertical alignment on `:` and `=`
- Safe primitives: `Safe_Str__Id`, `Safe_Str__Label`, `Safe_Str__Text`

## Usage

```python
from plantuml_exporter import MGraph__Export__PlantUML

exporter = MGraph__Export__PlantUML(
    graph = mgraph.graph                                                           ,
    data  = mgraph.data()                                                          ,
    index = mgraph.index()                                                         )

puml_code = (exporter
             .set_title('My Graph')
             .left_to_right()
             .set_show_node_value(True)
             .render())

print(puml_code)
# @startuml
# skinparam backgroundColor transparent
# skinparam shadowing false
# left to right direction
# title My Graph
#
# card "<<Node>>\nvalue" as n_abc123
# card "<<Node>>\nother" as n_def456
#
# n_abc123 --> n_def456 : predicate
# @enduml
```

## Configuration Objects

All inherit from `Type_Safe`:

```python
class PlantUML__Config(Type_Safe):
    graph                : PlantUML__Config__Graph            # direction, title, background
    node                 : PlantUML__Config__Node             # shape, colors
    edge                 : PlantUML__Config__Edge             # style, colors
    display              : PlantUML__Config__Display          # what to show

class PlantUML__Config__Display(Type_Safe):
    show_node_id         : bool                               = False
    show_node_type       : bool                               = True
    show_node_value      : bool                               = True
    show_edge_predicate  : bool                               = True
    show_edge_type       : bool                               = False
    wrap_at              : int                                = 40
```

## Context Mechanism

Uses `self.context.nodes` and `self.context.edges` to store rendered statements:

```python
class PlantUML__Context(Type_Safe):
    nodes                : List[str]                          # rendered node statements
    edges                : List[str]                          # rendered edge statements
```

## Non-Goals (v1)

- ❌ PNG rendering (use external PlantUML server)
- ❌ DOT-level layout tuning (ranksep, splines)
- ❌ Subgraph clustering
- ❌ Server integration

## References

- OSBot-Utils Type_Safe primitives
- MGraph-DB DOT exporter (architecture baseline)
- PlantUML language reference
