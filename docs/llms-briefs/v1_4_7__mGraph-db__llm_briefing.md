# MGraph-DB: Type-Safe Graph Database Framework - LLM Briefing

**Version**: v1.4.7  
**Last Updated**: 2nd December 2025  
**Repository**: owasp-sbot/MGraph-DB

## Executive Summary

MGraph-DB is a sophisticated, type-safe graph database framework built in Python using the OSBot-Utils Type_Safe system. It provides a layered architecture for creating, querying, and manipulating graph data structures with full runtime type checking, comprehensive indexing, and powerful visualization capabilities. The framework is designed for building domain-specific graph applications with strong type guarantees and elegant APIs.

**Key v1.4.7 Enhancements:**
- **Path Support**: Optional string-based path identifiers (`node_path`, `edge_path`, `graph_path`) for REST-friendly graph element classification
- **Enhanced Indexing**: Complete accessor methods, string-based type queries, predicate indexing with flexible parameters, and comprehensive statistics
- **Dual Interface Design**: Type-based methods (for Python) alongside string-based methods (for REST APIs)

## Core Architecture: Four-Layer Design

MGraph-DB uses a clean separation of concerns across four distinct layers:

### 1. Schema Layer (`schemas/`)
- **Purpose**: Pure data structures with zero business logic
- **Inherits**: All classes inherit from `Type_Safe`
- **Key Classes**:
  - `Schema__MGraph__Graph`: Complete graph structure with nodes, edges, metadata, and optional `graph_path`
  - `Schema__MGraph__Node`: Node definition with typed data and optional `node_path`
  - `Schema__MGraph__Edge`: Edge definition with relationships and optional `edge_path`
  - `Schema__MGraph__Node__Value`: Specialized node for storing primitive values
  - `Schema__MGraph__Index__Data`: Index structures for fast lookups including path-based indexes

**Critical Schema Rules**:
```python
# ✓ CORRECT - Pure schema
class Schema__MGraph__Node(Type_Safe):
    node_data : Schema__MGraph__Node__Data
    node_id   : Node_Id
    node_path : Node_Path                    = None      # NEW: Optional path identifier
    node_type : Type['Schema__MGraph__Node'] = None

# ✗ WRONG - No business logic in schemas
class Schema__MGraph__Node(Type_Safe):
    node_id: Node_Id
    
    def connect_to(self, other):  # NO! Business logic belongs in Model or Domain
        pass
```

### 2. Model Layer (`models/`)
- **Purpose**: Basic CRUD operations and direct data manipulation
- **Key Classes**:
  - `Model__MGraph__Graph`: Graph operations (add/delete nodes/edges)
  - `Model__MGraph__Node`: Node operations
  - `Model__MGraph__Edge`: Edge operations

**Model Layer Example**:
```python
class Model__MGraph__Graph(Type_Safe):
    data       : Schema__MGraph__Graph
    model_types: Model__MGraph__Types
    
    def add_node(self, node: Schema__MGraph__Node) -> Model__MGraph__Node:
        self.data.nodes[node.node_id] = node
        return self.model_types.node_model_type(data=node)
    
    def delete_node(self, node_id: Node_Id) -> bool:
        if node_id not in self.data.nodes:
            return False
        # Remove node and connected edges
        del self.data.nodes[node_id]
        return True
```

### 3. Domain Layer (`domain/`)
- **Purpose**: High-level business logic and graph domain operations
- **Key Classes**:
  - `Domain__MGraph__Graph`: Rich graph manipulation API
  - `Domain__MGraph__Node`: Node domain operations with edge traversal
  - `Domain__MGraph__Edge`: Edge domain operations

**Domain Layer Provides**:
- Graph traversal methods
- Node/edge relationship management
- High-level graph construction patterns
- Domain-specific operations

### 4. Action Layer (`actions/`)
- **Purpose**: Complex operations, algorithms, and utilities
- **Key Components**:
  - `MGraph__Edit`: Graph editing operations with index maintenance (including path support)
  - `MGraph__Data`: Data access and statistics
  - `MGraph__Index`: Comprehensive indexing system with path and predicate support
  - `MGraph__Index__Values`: Value node indexing with hash-based lookups
  - `MGraph__Builder`: Fluent API for graph construction
  - `MGraph__Export`: Multiple export formats
  - `MGraph__Values`: Value node management
  - `MGraph__Screenshot`: Visualization generation
  - `MGraph__Type__Resolver`: Type resolution with defaults handling

## The MGraph Main Class

The `MGraph` class is the primary user-facing API:

```python
class MGraph(Type_Safe):
    graph           : Domain__MGraph__Graph
    query_class     : Type[MGraph__Query]
    edit_class      : Type[MGraph__Edit]
    screenshot_class: Type[MGraph__Screenshot]
    
    def builder(self)     -> MGraph__Builder      # Fluent graph construction
    def data(self)        -> MGraph__Data         # Data access
    def edit(self)        -> MGraph__Edit         # Editing operations
    def export(self)      -> MGraph__Export       # Export to various formats
    def index(self)       -> MGraph__Index        # Access index
    def query(self)       -> MGraph__Query        # Query interface
    def values(self)      -> MGraph__Values       # Value node operations
    def screenshot(self)  -> MGraph__Screenshot   # Visualization
```

## Core Concepts

### Nodes and Edges

**Node Structure**:
```python
class Schema__MGraph__Node(Type_Safe):
    node_data : Schema__MGraph__Node__Data        # User-defined data
    node_id   : Node_Id                           # Unique identifier
    node_path : Node_Path                = None   # Optional path identifier
    node_type : Type['Schema__MGraph__Node'] = None  # Runtime type info
```

**Edge Structure**:
```python
class Schema__MGraph__Edge(Type_Safe):
    edge_id      : Edge_Id
    edge_data    : Schema__MGraph__Edge__Data      = None   # User-defined data
    edge_path    : Edge_Path                       = None   # Optional path identifier
    edge_type    : Type['Schema__MGraph__Edge']    = None   # Runtime type info
    edge_label   : Schema__MGraph__Edge__Label     = None   # Optional semantic label
    from_node_id : Node_Id                         = None
    to_node_id   : Node_Id                         = None
```

**Edge Labels** (Semantic Relationships):
```python
class Schema__MGraph__Edge__Label(Type_Safe):
    incoming  : Safe_Id = None    # How target sees the relationship
    outgoing  : Safe_Id = None    # How source sees the relationship
    predicate : Safe_Id = None    # Semantic relationship type
```

### Path Identifiers (New in v1.4.7)

Paths provide REST-friendly string-based identification that coexists with Python type fields:

```python
# Path primitive types
class Safe_Str__Graph__Path(Safe_Str):
    """Safe string for graph element paths.
    
    Allowed characters: a-zA-Z0-9, _, -, ., :, []
    Max length: 512 characters
    """
    regex           = re.compile(r'[^a-zA-Z0-9_\-.:\[\]]')
    max_length      = 512
    allow_empty     = True

class Node_Path(Safe_Str__Graph__Path): pass  # For nodes
class Edge_Path(Safe_Str__Graph__Path): pass  # For edges
class Graph_Path(Safe_Str__Graph__Path): pass # For graphs
```

**Path Examples**:
```python
# Document graphs (HTML, XML)
node_path = Node_Path("html.body.div.p[1]")

# Hierarchical data
node_path = Node_Path("config.database.connection.timeout")

# Indexed positions
node_path = Node_Path("table.row[5].cell[3]")

# Namespaced references
edge_path = Edge_Path("relationship.contains")
```

**Using Paths**:
```python
# Create nodes with paths
node = mgraph.edit().new_node(
    node_type=Schema__MGraph__Node,
    node_path=Node_Path("html.body.div")
)

# Create edges with paths
edge = mgraph.edit().new_edge(
    from_node_id=node1.node_id,
    to_node_id=node2.node_id,
    edge_path=Edge_Path("contains.child")
)

# Update paths on existing elements
mgraph.edit().set_node_path(node_id, Node_Path("new.path"))
mgraph.edit().set_edge_path(edge_id, Edge_Path("new.edge.path"))

# Query by path
node_ids = mgraph.index().get_nodes_by_path(Node_Path("html.body"))
edge_ids = mgraph.index().get_edges_by_path(Edge_Path("relationship.contains"))
```

### Value Nodes: The Unique System

MGraph-DB has a specialized system for storing primitive values as nodes with **automatic uniqueness enforcement**:

```python
class Schema__MGraph__Node__Value(Schema__MGraph__Node):
    node_data : Schema__MGraph__Node__Value__Data

class Schema__MGraph__Node__Value__Data(Type_Safe):
    value      : str        # Raw value stored as string
    key        : str        # Optional unique key
    value_type : Type       # Python type of the value
```

**How Value Uniqueness Works**:
1. Each value is hashed based on: `node_type + value_type + value + key`
2. Hash stored in `MGraph__Index__Values` 
3. Duplicate values automatically reference the same node
4. Enables efficient value-based queries and prevents duplication

**Value Node Usage**:
```python
# These three operations all reference the SAME node
node1 = mgraph.edit().new_value("hello")
node2 = mgraph.edit().new_value("hello")
node3 = mgraph.values().get_or_create("hello")

assert node1.node_id == node2.node_id == node3.node_id  # True!
```

## The Indexing System

MGraph-DB maintains comprehensive indexes for O(1) lookups:

### Main Index (`MGraph__Index`)

```python
class Schema__MGraph__Index__Data(Type_Safe):
    # Node indexes
    nodes_by_type                  : Dict[str, Set[Node_Id]]
    nodes_by_path                  : Dict[Node_Path, Set[Node_Id]]     # NEW: path -> node_ids
    nodes_types                    : Dict[Node_Id, str]
    
    # Edge indexes
    edges_by_type                  : Dict[str, Set[Edge_Id]]
    edges_by_path                  : Dict[Edge_Path, Set[Edge_Id]]     # NEW: path -> edge_ids
    edges_types                    : Dict[Edge_Id, str]
    edges_to_nodes                 : Dict[Edge_Id, tuple[Node_Id, Node_Id]]
    
    # Relationship indexes
    nodes_to_outgoing_edges        : Dict[Node_Id, Set[Edge_Id]]
    nodes_to_incoming_edges        : Dict[Node_Id, Set[Edge_Id]]
    nodes_to_outgoing_edges_by_type: Dict[Node_Id, Dict[str, Set[Edge_Id]]]
    nodes_to_incoming_edges_by_type: Dict[Node_Id, Dict[str, Set[Edge_Id]]]
    
    # Semantic indexes
    edges_predicates               : Dict[Edge_Id, Safe_Id]
    edges_by_predicate             : Dict[Safe_Id, Set[Edge_Id]]
    edges_by_incoming_label        : Dict[Safe_Id, Set[Edge_Id]]
    edges_by_outgoing_label        : Dict[Safe_Id, Set[Edge_Id]]
```

### Index Accessor Methods (Enhanced in v1.4.7)

All index data is now accessible via consistent methods:

```python
# Raw data accessors
index.edges_to_nodes()                    # Dict[Edge_Id, tuple[Node_Id, Node_Id]]
index.edges_by_type()                     # Dict[str, Set[Edge_Id]]
index.edges_by_path()                     # Dict[Edge_Path, Set[Edge_Id]]
index.nodes_by_type()                     # Dict[str, Set[Node_Id]]
index.nodes_by_path()                     # Dict[Node_Path, Set[Node_Id]]
index.nodes_to_incoming_edges()           # Dict[Node_Id, Set[Edge_Id]]
index.nodes_to_incoming_edges_by_type()   # Dict[Node_Id, Dict[str, Set[Edge_Id]]]
index.nodes_to_outgoing_edges()           # Dict[Node_Id, Set[Edge_Id]]
index.nodes_to_outgoing_edges_by_type()   # Dict[Node_Id, Dict[str, Set[Edge_Id]]]

# Predicate accessors (NEW)
index.edges_predicates()                  # Dict[Edge_Id, Safe_Id]
index.edges_by_predicate_all()            # Dict[Safe_Id, Set[Edge_Id]]
index.edges_by_incoming_label()           # Dict[Safe_Id, Set[Edge_Id]]
index.edges_by_outgoing_label()           # Dict[Safe_Id, Set[Edge_Id]]
```

### String-Based Type Queries (New in v1.4.7)

For REST API compatibility, type queries can now use string names:

```python
# Type-based (Python usage)
node_ids = mgraph.index().get_nodes_by_type(MyNodeType)
edge_ids = mgraph.index().get_edges_by_type(MyEdgeType)

# Path-based (REST-friendly)
node_ids = mgraph.index().get_nodes_by_path(Node_Path("html.body"))
edge_ids = mgraph.index().get_edges_by_path(Edge_Path("contains"))

# All paths
all_node_paths = mgraph.index().get_all_node_paths()  # Set[Node_Path]
all_edge_paths = mgraph.index().get_all_edge_paths()  # Set[Edge_Path]
```

### Value Index (`MGraph__Index__Values`)

```python
class Schema__MGraph__Value__Index__Data(Type_Safe):
    hash_to_node   : Dict[str, Node_Id]       # value_hash -> node_id
    node_to_hash   : Dict[Node_Id, str]       # node_id -> value_hash
    values_by_type : Dict[Type, Set[str]]     # type -> set of hashes
    type_by_value  : Dict[str, Type]          # hash -> type
```

**Index Usage Examples**:
```python
# Get all nodes of a specific type
node_ids = mgraph.index().get_nodes_by_type(MyNodeType)

# Get outgoing edges for a node
edges = mgraph.index().get_node_outgoing_edges(node)
edge_ids = mgraph.index().get_node_id_outgoing_edges(node_id)

# Get incoming edges for a node
incoming_edge_ids = mgraph.index().get_node_id_incoming_edges(node_id)

# Find value node
node_id = mgraph.index().values_index.get_node_id_by_value(
    value_type=str, 
    value="hello"
)

# Get nodes by predicate relationship (accepts str or Safe_Id)
target_nodes = mgraph.index().get_nodes_by_predicate(
    from_node_id=node_id,
    predicate="has_property"  # or Safe_Id("has_property")
)

# Get edges by predicate (accepts str or Safe_Id)
edges = mgraph.index().get_edges_by_predicate("has_name")
outgoing = mgraph.index().get_node_outgoing_edges_by_predicate(node_id, "has_property")
incoming = mgraph.index().get_node_incoming_edges_by_predicate(node_id, "belongs_to")

# Path-based queries
node_ids = mgraph.index().get_nodes_by_path(Node_Path("config.database"))
edge_ids = mgraph.index().get_edges_by_path(Edge_Path("relationship.contains"))
node_path = mgraph.index().get_node_path(node_id)  # Returns Optional[Node_Path]
edge_path = mgraph.index().get_edge_path(edge_id)  # Returns Optional[Edge_Path]
count = mgraph.index().count_nodes_by_path(Node_Path("html.body"))
exists = mgraph.index().has_node_path(Node_Path("config.settings"))
```

### Index Statistics (Enhanced in v1.4.7)

```python
stats = mgraph.index().stats()

# Returns comprehensive statistics:
{
    'index_data': {
        'edge_to_nodes'        : 42,
        'edges_by_type'        : {'Schema__MGraph__Edge': 42},
        'edges_by_path'        : {'contains': 10, 'references': 5},   # NEW
        'nodes_by_type'        : {'Schema__MGraph__Node': 50},
        'nodes_by_path'        : {'html.body': 5, 'config': 3},       # NEW
        'node_edge_connections': {
            'total_nodes'      : 50,
            'avg_incoming_edges': 2,
            'avg_outgoing_edges': 2,
            'max_incoming_edges': 10,
            'max_outgoing_edges': 8
        }
    },
    'summary': {
        'total_nodes'      : 50,
        'total_edges'      : 42,
        'total_predicates' : 5,
        'unique_node_paths': 8,                                       # NEW
        'unique_edge_paths': 3,                                       # NEW
        'nodes_with_paths' : 15,                                      # NEW
        'edges_with_paths' : 10                                       # NEW
    },
    'paths': {                                                        # NEW section
        'node_paths': {'html.body': 5, 'config': 3},
        'edge_paths': {'contains': 10, 'references': 5}
    }
}
```

### Index Rebuild (New in v1.4.7)

```python
# Rebuild index via MGraph__Edit
fresh_index = mgraph.edit().rebuild_index()

# The index is automatically maintained during edit operations
mgraph.edit().add_node(node)      # Automatically updates index
mgraph.edit().delete_node(node_id) # Automatically removes from index
```

## Graph Construction: The Builder Pattern

The `MGraph__Builder` provides a fluent API for constructing graphs:

```python
# Create a simple graph
with mgraph.builder() as builder:
    builder.add_node("Root")                          # Creates root node
           .add_connected_node("Child 1")             # Adds and connects child
           .add_connected_node("Grandchild 1")        # Grandchild of Child 1
           .up()                                      # Back to Child 1
           .add_connected_node("Grandchild 2")        # Second grandchild
           .root()                                    # Back to root
           .add_connected_node("Child 2")             # Second child of root

# Using predicates (semantic relationships)
builder.add_node("Person")
       .add_predicate("name", "John", node_type=Schema__MGraph__Node__Value)
       .root()
       .add_predicate("age", 30)
       .root()
       .add_predicate("city", "London")

# Using edge types
builder.add_node("Document")
       .add_connected_node("Section", edge_type=Edge__Contains)
       .add_connected_node("Paragraph", edge_type=Edge__Contains)

# Navigation
builder.node_up()    # Move to parent
builder.root()       # Return to root
builder.up()         # Alias for node_up()
```

**Builder Features**:
- Maintains current node context
- Tracks history for navigation
- Supports predicate-based connections
- Type-safe edge creation
- Unique value enforcement via `config__unique_values = True`

## Query System: Powerful Graph Queries

The query system (`MGraph__Query`) provides chainable operations with view management:

### Query Architecture

```python
class MGraph__Query(Type_Safe):
    mgraph_data  : MGraph__Data                    # Access to graph data
    mgraph_index : MGraph__Index                   # Access to indexes
    query_views  : Model__MGraph__Query__Views     # View history management
    root_nodes   : Set[Node_Id]                    # Starting nodes
```

### View System

Every query operation creates a new **view** (snapshot of node/edge IDs):

```python
class Schema__MGraph__Query__View(Type_Safe):
    view_id   : Obj_Id
    view_data : Schema__MGraph__Query__View__Data

class Schema__MGraph__Query__View__Data(Type_Safe):
    nodes_ids       : Set[Node_Id]             # Nodes in this view
    edges_ids       : Set[Edge_Id]             # Edges in this view
    previous_view_id: Optional[Obj_Id]         # Previous view (for history)
    next_view_ids   : Set[Obj_Id]              # Possible next views
    query_operation : str                       # Operation that created view
    query_params    : Dict[str, Any]            # Parameters used
    timestamp       : Timestamp_Now             # When created
```

### Basic Query Operations

```python
# Filter by node type
query.by_type(MyNodeType)

# Find nodes with specific value
query.with_node_value("hello")
query.with_node_value("hello", edge_type=Edge__HasProperty)

# Collect results
nodes = query.collect()      # Returns List[Domain__MGraph__Node]
first = query.first()        # Returns first node or None
value = query.value()        # Returns value of first node
count = query.count()        # Returns count of nodes
exists = query.exists()      # Returns bool

# Navigation
query.go_back()              # Go to previous view
query.go_forward()           # Go to next view (if multiple branches)

# Statistics
stats = query.stats()        # View and graph statistics
query.print_stats()          # Pretty print statistics
```

### Advanced Query Operations

**Adding Nodes to View**:
```python
# Add specific node
query.add().add_node_id(node_id)

# Add nodes with specific value
query.add().add_node_with_value("some_value")

# Add nodes of specific type
query.add().add_nodes_with_type(MyNodeType)

# Add nodes connected by specific edge type
query.add().add_nodes_with_outgoing_edge(Edge__HasProperty)
query.add().add_nodes_with_incoming_edge(Edge__BelongsTo)
```

**Graph Expansion**:
```python
# Add outgoing edges (expands graph by one level)
query.add().add_outgoing_edges()

# Add outgoing edges with depth
query.add().add_outgoing_edges(depth=3)  # Expands 3 levels deep
```

**Navigation**:
```python
# Navigate to connected nodes
query.navigate().to_connected_nodes(
    edge_type=Edge__HasProperty,
    direction='outgoing'  # or 'incoming'
)
```

### Query View Export

Export current query view as independent graph:

```python
# Export creates a new graph with only the nodes/edges in current view
new_graph = query.export_view()

# This is a complete, independent MGraph instance
new_mgraph = MGraph(graph=new_graph)

# Can be queried, visualized, exported separately
new_mgraph.screenshot().save_to('view.png').dot()
```

## Visualization and Export

### Screenshot System

Generate PNG visualizations using Graphviz DOT:

```python
# Basic screenshot
mgraph.screenshot().save_to('graph.png').dot()

# Configure visualization
with mgraph.screenshot() as shot:
    with shot.export().export_dot() as dot:
        # Node display
        dot.show_node__id()
        dot.show_node__type()
        dot.show_node__value()
        dot.show_node__value__key()
        dot.show_node__value__type()
        
        # Edge display
        dot.show_edge__id()
        dot.show_edge__type()
        dot.show_edge__predicate()
        
        # Layout
        dot.set_graph__layout_engine__dot()   # or neato, circo, fdp, sfdp, etc.
        dot.set_graph__rank_dir__lr()         # Left to right (or TB, BT, RL)
        dot.set_graph__margin(0.5)
        dot.set_graph__node_sep(1.0)
        dot.set_graph__rank_sep(0.5)
        
        # Styling
        dot.set_node__shape__type__box()      # or circle, ellipse, diamond, etc.
        dot.set_node__shape__rounded()
        dot.set_node__fill_color("#E8E8E8")
        dot.set_edge__color("blue")
        dot.set_edge__arrow_head__vee()       # or dot, tee, none, diamond, etc.
        
        # Title
        dot.set_graph__title("My Graph")
        dot.set_graph__title__font__size(16)
        dot.set_graph__background__color("#FFFFFF")
```

**Advanced Styling**:
```python
# Style by node type
dot.set_node__type_fill_color(MyNodeType, "lightblue")
dot.set_node__type_font_size(MyNodeType, 14)
dot.set_node__type_shape(MyNodeType, "diamond")
dot.set_node__type_rounded(MyNodeType)

# Style by edge type
dot.set_edge__type_color(Edge__Contains, "green")
dot.set_edge__type_style(Edge__Contains, "dashed")

# Style nodes based on edge relationships
dot.set_edge_to_node__type_fill_color(Edge__Contains, "yellow")
dot.set_edge_from_node__type_fill_color(Edge__Contains, "orange")

# Style value nodes by value type
dot.set_value_type_fill_color(str, "lightgreen")
dot.set_value_type_shape(int, "circle")
dot.set_value_type_font_color(str, "#333333")
```

### Export Formats

MGraph-DB supports multiple export formats:

```python
# DOT (Graphviz)
dot_code = mgraph.export().to__dot()

# Mermaid
mermaid = mgraph.export().to__mermaid()

# GraphML
graphml = mgraph.export().to__graphml()

# Cypher (Neo4j)
cypher = mgraph.export().to__cypher()

# JSON (compressed)
json_data = mgraph.export().to__json()

# Full MGraph JSON (with type registry)
mgraph_json = mgraph.export().to__mgraph_json()

# XML
xml = mgraph.export().to__xml()

# CSV (nodes and edges)
csv_data = mgraph.export().to__csv()  # Returns dict with 'nodes.csv', 'edges.csv'

# Other formats
mgraph.export().to__gexf()       # GEXF
mgraph.export().to__tgf()        # Trivial Graph Format
mgraph.export().to__turtle()     # RDF Turtle
mgraph.export().to__ntriples()   # N-Triples
```

### Tree Export

Export graph as hierarchical tree:

```python
# Get tree exporter
tree_export = mgraph.export().export_tree_values(
    root_nodes_ids=[root_node_id]
)

# Generate tree structure
tree_dict = tree_export.format_output()

# Print as text
tree_text = tree_export.as_text([root_node_id])
print(tree_text)

# Output example:
# Root
#     has_property:
#         name
#         age
#     contains:
#         Section 1
#             Paragraph 1
#             Paragraph 2
```

## Graph Diffing

Compare two graphs to find differences:

```python
from mgraph_db.mgraph.actions.MGraph__Diff import MGraph__Diff

diff = MGraph__Diff(graph_a=graph1, graph_b=graph2)
result = diff.diff_graphs()

# Result structure
result.nodes_added       # Set[Node_Id]
result.nodes_removed     # Set[Node_Id]
result.nodes_modified    # Dict[Node_Id, Schema__MGraph__Node__Changes]
result.edges_added       # Set[Edge_Id]
result.edges_removed     # Set[Edge_Id]
result.edges_modified    # Dict[Edge_Id, Schema__MGraph__Edge__Changes]
result.nodes_count_diff  # int
result.edges_count_diff  # int
```

**Value-Based Diffing**:
```python
from mgraph_db.mgraph.actions.MGraph__Diff__Values import MGraph__Diff__Values

diff = MGraph__Diff__Values(graph1=mgraph1, graph2=mgraph2)
result = diff.compare(value_types=[str, int, MyValueType])

result.added_values      # Dict[Type, set[str]]
result.removed_values    # Dict[Type, set[str]]
```

**Visualize Diff**:
```python
from mgraph_db.mgraph.views.MGraph__View__Diff__Values import MGraph__View__Diff__Values

view = MGraph__View__Diff__Values(diff=result, mgraph=MGraph())
diff_graph = view.create_graph()
diff_graph.screenshot().save_to('diff.png').dot()
```

## Custom Types and Extensions

### Creating Custom Node Types

```python
# 1. Define your node data schema
class Schema__MyApp__Node__Document__Data(Schema__MGraph__Node__Data):
    title     : Safe_Str__Text
    author    : Safe_Str__Username
    created_at: Timestamp_Now

# 2. Define your node type
class Schema__MyApp__Node__Document(Schema__MGraph__Node):
    node_data: Schema__MyApp__Node__Document__Data

# 3. Use it
doc_data = Schema__MyApp__Node__Document__Data(
    title=Safe_Str__Text("My Document"),
    author=Safe_Str__Username("john_doe")
)
doc_node = Schema__MyApp__Node__Document(
    node_data=doc_data,
    node_type=Schema__MyApp__Node__Document
)
mgraph.edit().add_node(doc_node)
```

### Creating Custom Edge Types

```python
# 1. Define edge data (if needed)
class Schema__MyApp__Edge__Authored__Data(Schema__MGraph__Edge__Data):
    date: Timestamp_Now

# 2. Define edge type
class Schema__MyApp__Edge__Authored(Schema__MGraph__Edge):
    edge_data: Schema__MyApp__Edge__Authored__Data

# 3. Use it
mgraph.edit().new_edge(
    edge_type=Schema__MyApp__Edge__Authored,
    from_node_id=person_node_id,
    to_node_id=document_node_id
)
```

### Creating Custom Graph Types

```python
# 1. Define graph-level data
class Schema__MyApp__Graph__Data(Schema__MGraph__Graph__Data):
    version: Safe_Str__Version
    owner  : Safe_Str__Username

# 2. Define type configuration
class Schema__MyApp__Types(Schema__MGraph__Types):
    edge_type       : Type[Schema__MGraph__Edge]       = Schema__MyApp__Edge__Authored
    graph_data_type : Type[Schema__MGraph__Graph__Data] = Schema__MyApp__Graph__Data
    node_type       : Type[Schema__MGraph__Node]       = Schema__MyApp__Node__Document
    node_data_type  : Type[Schema__MGraph__Node__Data] = Schema__MyApp__Node__Document__Data

# 3. Create graph with custom types
graph_data = Schema__MyApp__Graph__Data(
    version=Safe_Str__Version("1.0.0"),
    owner=Safe_Str__Username("john_doe")
)

graph_schema = Schema__MGraph__Graph(
    schema_types=Schema__MyApp__Types(),
    graph_type=Schema__MGraph__Graph,
    graph_data=graph_data
)
```

## Common Patterns

### Pattern 1: Document with Properties

```python
# Create document node
doc = mgraph.builder().add_node("Document")

# Add properties using predicates
builder = mgraph.builder()
builder.set_current_node(doc)
builder.add_predicate("title", "My Document")
       .root()
       .add_predicate("author", "John Doe")
       .root()
       .add_predicate("date", "2025-01-01")

# Query by property
docs_by_john = (mgraph.query()
                      .by_type(Schema__MGraph__Node)
                      .with_node_value("John Doe", edge_type=Edge__HasProperty))
```

### Pattern 2: Hierarchical Structure

```python
# Build hierarchy
builder = mgraph.builder()
root = builder.add_node("Organization")

builder.add_connected_node("Engineering", edge_type=Edge__Contains)
       .add_connected_node("Backend Team")
       .add_connected_node("Alice")
       .up()
       .add_connected_node("Bob")
       .up().up()
       .add_connected_node("Frontend Team")
       .add_connected_node("Carol")

# Query hierarchy
engineering = mgraph.query().with_node_value("Engineering").first()
teams = (mgraph.query()
               .add().add_node_id(engineering.node_id)
               .add().add_outgoing_edges(depth=2))
```

### Pattern 3: Path-Based Document Structure (New in v1.4.7)

```python
# Create document structure with paths
with mgraph.edit() as edit:
    html = edit.new_node(node_path=Node_Path("html"))
    body = edit.new_node(node_path=Node_Path("html.body"))
    div1 = edit.new_node(node_path=Node_Path("html.body.div[0]"))
    div2 = edit.new_node(node_path=Node_Path("html.body.div[1]"))
    
    # Connect with path-labeled edges
    edit.new_edge(from_node_id=html.node_id, to_node_id=body.node_id,
                  edge_path=Edge_Path("contains.child"))
    edit.new_edge(from_node_id=body.node_id, to_node_id=div1.node_id,
                  edge_path=Edge_Path("contains.child"))

# Query by path
body_node_ids = mgraph.index().get_nodes_by_path(Node_Path("html.body"))
```

### Pattern 4: Value-Based Relationships

```python
# Create person and city nodes
person = mgraph.edit().new_value("Alice")
city   = mgraph.edit().new_value("London")

# Connect with predicate
edge = mgraph.edit().get_or_create_edge(
    from_node_id=person.node_id,
    to_node_id=city.node_id,
    predicate="lives_in"
)

# Query people in London
london_node = mgraph.query().with_node_value("London").first()
people = (mgraph.query()
                .add().add_node_id(london_node.node_id)
                .navigate().to_connected_nodes(direction='incoming'))
```

### Pattern 5: Graph Analysis

```python
# Get all nodes by type
doc_nodes = mgraph.query().by_type(Schema__MyApp__Node__Document).collect()

# Find isolated nodes (no connections)
all_nodes = set(mgraph.data().nodes_ids())
connected_nodes = set()
for edge in mgraph.data().edges():
    connected_nodes.add(edge.from_node_id())
    connected_nodes.add(edge.to_node_id())
isolated = all_nodes - connected_nodes

# Find hub nodes (most connections)
hub_scores = {}
for node_id in mgraph.data().nodes_ids():
    outgoing = len(mgraph.index().get_node_id_outgoing_edges(node_id))
    incoming = len(mgraph.index().get_node_id_incoming_edges(node_id))
    hub_scores[node_id] = outgoing + incoming

most_connected = max(hub_scores, key=hub_scores.get)
```

## Integration Examples

### Example 1: Document Management System

```python
# Define types
class Doc_Node(Schema__MGraph__Node):
    pass

class Doc_Data(Schema__MGraph__Node__Data):
    title: Safe_Str__Text
    content: Safe_Str__Text

class Edge__HasTag(Schema__MGraph__Edge):
    pass

# Create graph
mgraph = MGraph()

# Add documents
doc1 = mgraph.edit().new_node(
    node_type=Doc_Node,
    title="Introduction",
    content="This is the intro..."
)

# Add tags as value nodes
tag_python = mgraph.edit().new_value("python")
tag_tutorial = mgraph.edit().new_value("tutorial")

# Connect documents to tags
mgraph.edit().connect_nodes(doc1, tag_python, edge_type=Edge__HasTag)
mgraph.edit().connect_nodes(doc1, tag_tutorial, edge_type=Edge__HasTag)

# Query: Find all documents with "python" tag
python_docs = (mgraph.query()
                     .with_node_value("python")
                     .navigate().to_connected_nodes(
                         edge_type=Edge__HasTag,
                         direction='incoming'
                     )
                     .collect())
```

### Example 2: Dependency Graph

```python
# Define types
class Package_Node(Schema__MGraph__Node):
    pass

class Edge__DependsOn(Schema__MGraph__Edge):
    pass

# Build dependency graph
mgraph = MGraph()
builder = mgraph.builder()

# Create packages
app = builder.add_node("myapp")
builder.add_connected_node("requests", edge_type=Edge__DependsOn)
       .add_connected_node("urllib3", edge_type=Edge__DependsOn)
       .up().up()
       .add_connected_node("pandas", edge_type=Edge__DependsOn)
       .add_connected_node("numpy", edge_type=Edge__DependsOn)

# Find all dependencies (recursive)
all_deps = (mgraph.query()
                  .with_node_value("myapp")
                  .add().add_outgoing_edges(depth=10)
                  .collect())

# Visualize
mgraph.screenshot().save_to('dependencies.png').dot()
```

## Best Practices

### 1. Use Type_Safe Primitives

Never use raw `str`, `int`, `float`:

```python
# ❌ BAD
class MyNode(Schema__MGraph__Node__Data):
    name: str           # Vulnerable to injection
    age: int            # Can overflow
    balance: float      # Precision errors

# ✓ GOOD
class MyNode(Schema__MGraph__Node__Data):
    name: Safe_Str__Username     # Sanitized
    age: Safe_UInt__Age          # Range-checked
    balance: Safe_Float__Money   # Exact arithmetic
```

### 2. Leverage Value Nodes for Uniqueness

```python
# ✓ GOOD - Automatic deduplication
tag1 = mgraph.edit().new_value("python")
tag2 = mgraph.edit().new_value("python")
assert tag1.node_id == tag2.node_id  # Same node!

# ❌ BAD - Manual deduplication
existing = mgraph.query().with_node_value("python").first()
if existing:
    tag = existing
else:
    tag = mgraph.edit().new_node(value="python")
```

### 3. Use Predicates for Semantic Relationships

```python
# ✓ GOOD - Semantic meaning clear
builder.add_predicate("author", "John Doe")
builder.add_predicate("published_date", "2025-01-01")

# ❌ BAD - Generic edges lose meaning
builder.connect_to("John Doe")
builder.connect_to("2025-01-01")
```

### 4. Use Paths for REST API Integration (New in v1.4.7)

```python
# ✓ GOOD - Paths enable REST-friendly queries
node = mgraph.edit().new_node(
    node_type=Schema__MGraph__Node,
    node_path=Node_Path("html.body.section[1]")
)

# REST clients can query by path string
node_ids = mgraph.index().get_nodes_by_path(Node_Path("html.body"))

# ❌ BAD - Relying solely on Python types for REST APIs
# REST clients cannot provide Python type objects
```

### 5. Index Management

```python
# ✓ GOOD - Use MGraph__Edit for automatic index updates
mgraph.edit().add_node(node)
mgraph.edit().delete_edge(edge_id)

# Rebuild index if needed
fresh_index = mgraph.edit().rebuild_index()

# ❌ BAD - Direct model manipulation bypasses index
mgraph.data().graph.model.add_node(node)  # Index not updated!
```

### 6. Query View Export for Subgraphs

```python
# ✓ GOOD - Export view as independent graph
filtered = mgraph.query().by_type(MyType)
subgraph = filtered.export_view()  # Complete independent graph

# ❌ BAD - Manually copying nodes/edges
new_graph = MGraph()
for node_id in filtered.nodes_ids():
    node = mgraph.data().node(node_id)
    new_graph.edit().add_node(node.node.data)
# This is tedious and error-prone
```

### 7. Builder for Construction, Query for Analysis

```python
# ✓ GOOD - Use builder for initial construction
with mgraph.builder() as b:
    b.add_node("Root").add_connected_node("Child")

# ✓ GOOD - Use query for analysis
results = mgraph.query().by_type(MyType).collect()

# ❌ BAD - Using query for construction
mgraph.query().add().add_node_id(new_id)  # Confusing
```

## Performance Considerations

### Index Maintenance

The index is automatically maintained by `MGraph__Edit`:

```python
# Adding nodes/edges automatically updates index
mgraph.edit().add_node(node)      # Updates nodes_by_type, nodes_by_path, etc.
mgraph.edit().add_edge(edge)      # Updates edges_to_nodes, edges_by_path, etc.

# Deleting also updates index
mgraph.edit().delete_node(node_id)  # Removes from all indexes
mgraph.edit().delete_edge(edge_id)  # Removes from all indexes

# Setting paths updates path indexes
mgraph.edit().set_node_path(node_id, Node_Path("new.path"))  # Updates nodes_by_path
```

### Value Node Performance

Value nodes use hash-based lookups (O(1)):

```python
# Fast lookups by value
node_id = mgraph.index().values_index.get_node_id_by_value(
    value_type=str,
    value="hello"
)  # O(1) lookup

# Fast lookups by hash
node_id = mgraph.index().values_index.get_node_id_by_hash(hash_value)  # O(1)
```

### Query View Performance

Views store only node/edge IDs, not the full data:

```python
# Creating a view is O(1) - just creates ID sets
query.by_type(MyType)

# Collecting results is O(n) where n is nodes in view
nodes = query.collect()
```

### Path Query Performance

Path-based indexes provide efficient lookups:

```python
# Path lookups are O(1)
node_ids = mgraph.index().get_nodes_by_path(Node_Path("html.body"))  # O(1)

# Path existence check is O(1)
exists = mgraph.index().has_node_path(Node_Path("config.settings"))  # O(1)
```

## Error Handling

MGraph-DB uses Type_Safe validation which catches errors at assignment:

```python
# Type errors caught immediately
node = Schema__MGraph__Node(
    node_data=Schema__MGraph__Node__Data(),
    node_id="not-an-obj-id"  # ❌ TypeError: expected Node_Id
)

# Invalid path characters caught
node_path = Node_Path("invalid/path")  # ❌ ValueError: invalid characters

# Missing required fields caught
edge = Schema__MGraph__Edge(
    edge_id=Edge_Id()
    # ❌ Missing from_node_id and to_node_id
)

# Invalid edge connections caught
mgraph.edit().new_edge(
    from_node_id=Node_Id(),  # Node doesn't exist
    to_node_id=Node_Id()     # ❌ ValueError: Node not found
)
```

## Troubleshooting

### Issue: "Node with ID X not found"

```python
# Check if node exists before referencing
if mgraph.data().node(node_id):
    # Safe to use
    edge = mgraph.edit().new_edge(from_node_id=node_id, ...)
```

### Issue: "Value already exists"

Value nodes are unique by design - this is expected:

```python
# Both reference same node - this is correct behavior
node1 = mgraph.edit().new_value("hello")
node2 = mgraph.edit().new_value("hello")
assert node1.node_id == node2.node_id
```

### Issue: Index out of sync

If index gets out of sync, rebuild it:

```python
# Rebuild index from graph
fresh_index = mgraph.edit().rebuild_index()
```

### Issue: Query returns empty results

Check view history:

```python
# See what operations were performed
stats = mgraph.query().stats()
print(stats['current_view'])

# Go back if needed
mgraph.query().go_back()
```

### Issue: Path not found

Paths are optional - check if set:

```python
# Check if node has a path
node_path = mgraph.index().get_node_path(node_id)
if node_path:
    print(f"Node path: {node_path}")
else:
    print("Node has no path set")
```

## Testing Utilities

Create test graphs easily:

```python
from mgraph_db.mgraph.utils.MGraph__Random_Graph import create_random_mgraph, create_empty_mgraph
from mgraph_db.mgraph.utils.MGraph__Static__Graph import MGraph__Static__Graph

# Empty graph
mgraph = create_empty_mgraph()

# Random graph
mgraph = create_random_mgraph(num_nodes=10, num_edges=20)

# Static patterns
linear = MGraph__Static__Graph.create_linear(num_nodes=5)
circular = MGraph__Static__Graph.create_circular(num_nodes=5)
star = MGraph__Static__Graph.create_star(num_spokes=5)
complete = MGraph__Static__Graph.create_complete(num_nodes=5)
```

## Code Style Requirements

When working with MGraph-DB, follow these Type_Safe conventions:

### Formatting Rules

```python
# ✓ CORRECT - Vertical alignment, multiple params
def create_edge(self, from_node : Node_Id                         ,  # Source node
                      to_node   : Node_Id                         ,  # Target node
                      edge_type : Type[Schema__MGraph__Edge] = None,  # Edge type
                      edge_path : Edge_Path                  = None   # Edge path
                ) -> Domain__MGraph__Edge:
    pass

# ✓ CORRECT - Inline if simple
def get_node(self, node_id: Node_Id) -> Domain__MGraph__Node:
    pass

# ❌ WRONG - PEP-8 style (don't use with MGraph-DB)
def create_edge(
    self,
    from_node,
    to_node,
    edge_type=None
):
    pass
```

### Type Annotations

```python
# ✓ CORRECT - Full type annotations
class MyNode(Type_Safe):
    node_id   : Node_Id
    node_path : Node_Path                        = None
    data      : Schema__MGraph__Node__Data
    neighbors : List[Node_Id]

# ❌ WRONG - Missing types
class MyNode(Type_Safe):
    node_id = Node_Id()
    data = None
    neighbors = []
```

### Method Structure

```python
# ✓ CORRECT - Aligned dict literals
node_data = {
    'node_id'  : Node_Id()                ,
    'node_type': Schema__MGraph__Node     ,
    'node_path': Node_Path("config.item") ,
    'value'    : "example"                ,
}

# ✓ CORRECT - Aligned method chains
result = (mgraph.query()
                .by_type(MyType)
                .with_node_value("example")
                .collect())
```

## Summary

MGraph-DB provides:

1. **Type-Safe Architecture**: Four clean layers (Schema/Model/Domain/Action)
2. **Comprehensive Indexing**: O(1) lookups for nodes, edges, values, predicates, and paths
3. **Path Support**: REST-friendly string-based element identification (new in v1.4.7)
4. **Value Node System**: Automatic uniqueness enforcement for primitive values
5. **Fluent Builder API**: Elegant graph construction with navigation
6. **Powerful Query System**: Chainable operations with view history
7. **Rich Visualization**: Multiple export formats and customizable DOT rendering
8. **Semantic Relationships**: Predicate-based edge labels
9. **Graph Diffing**: Compare graphs at node/edge or value level
10. **Extension Points**: Custom node/edge/graph types
11. **Type Safety**: Runtime validation catches errors at assignment
12. **REST API Ready**: String-based queries for service layer integration (new in v1.4.7)

When using MGraph-DB in your project:
- Inherit from appropriate base classes (Schema/Model/Domain layers)
- Use Type_Safe primitives (Safe_Id, Safe_Str__*, Node_Path, Edge_Path, etc.)
- Leverage value nodes for uniqueness
- Use predicates for semantic meaning
- Use paths for REST API integration and structural identification
- Follow the established code formatting style
- Let the index handle lookups
- Use builder for construction, query for analysis
- Export views for subgraph operations

The framework is designed for building sophisticated graph-based applications with strong type guarantees and elegant APIs, now with enhanced REST API support through path-based identification.
