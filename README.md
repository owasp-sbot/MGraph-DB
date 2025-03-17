# MGraph-DB: A Memory-based GraphDB for Python, GenAI, Semantic Web and Serverless

![Current Release](https://img.shields.io/badge/release-v1.2.13-blue)

> **QUICKSTART GUIDE**: For working code examples, check out our test suite at:
> ```
> tests/quickstart/test_README_examples.py
> ```
> This file contains executable versions of all examples shown below, providing a hands-on way to learn the library.

MGraph-DB is a high-performance, type-safe graph database implementation in Python, optimized for in-memory operations with JSON persistence. Its architecture makes it particularly well-suited for:

- **GenAI Applications**
  - Knowledge graph construction and querying
  - Semantic relationship modeling
  - Context management for LLMs
  - Graph-based reasoning systems

- **Semantic Web**
  - RDF data processing
  - Ontology management
  - Linked data applications
  - SPARQL-compatible queries

- **Serverless Deployments**
  - Quick cold starts with memory-first design
  - Efficient JSON serialization
  - Low memory footprint
  - Built-in serverless support via [MGraph_DB_Serverless](https://github.com/owasp-sbot/MGraph-DB-Serverless)

- **Python Ecosystem**
  - Native Python implementation
  - Full type safety and validation
  - Clean, Pythonic API
  - Rich integration capabilities

## Major Features

### Production-Ready Type System
- Complete implementation of the three-layer architecture (Domain, Model, Schema)
- Comprehensive runtime type checking across all layers
- Type-safe property accessors and method decorators
- Robust validation for nested data structures
- Clean class hierarchies with explicit interfaces

### Advanced Graph Operations
- High-performance in-memory graph operations
- Sophisticated query system with chainable operations
- Rich traversal capabilities with type filtering
- Flexible node and edge attribute management
- Comprehensive CRUD operations for graph elements

### Optimized Indexing System
- O(1) lookups for all core operations
- Multi-dimensional indexing (type, attribute, relationship)
- Efficient graph traversal support
- Advanced query optimization
- Index persistence and restoration

### Query System Enhancements
- View-based query results with navigation
- Rich filtering and traversal operations
- Chainable query interface
- Query result caching
- Query operation history tracking

### Export Capabilities
- Support for multiple export formats:
  - GraphML
  - DOT
  - Mermaid
  - RDF/Turtle
  - N-Triples
  - GEXF
  - TGF
  - Cypher
  - CSV
  - JSON

### Visualization Support
- Integration with common visualization libraries
- Custom layout algorithms
- Interactive graph exploration
- Support for large graph visualization
- Multiple visualization format exports

## Quick Start

Here's a simple example showing basic graph operations:

```python
def test_basic_graph_operations():
    from mgraph_db.mgraph.MGraph import MGraph
    
    # Create a new graph
    mgraph = MGraph()
    
    with mgraph.edit() as edit:
        # Create two nodes
        node1 = edit.new_node(node_data={"value": "First Node"})
        node2 = edit.new_node(node_data={"value": "Second Node"})
        
        # Connect nodes with an edge
        edge = edit.new_edge(from_node_id=node1.node_id, 
                            to_node_id=node2.node_id)
        
        # Verify nodes and edge were created
        assert node1.node_id is not None
        assert node2.node_id is not None
        assert edge.edge_id is not None
    
    # Query the graph
    with mgraph.data() as data:
        nodes = data.nodes()
        edges = data.edges()
        
        assert len(nodes) == 2
        assert len(edges) == 1
```

## Use Cases

### GenAI Integration

```python
def test_genai_integration():
    from mgraph_db.mgraph.MGraph import MGraph
    
    mgraph = MGraph()
    with mgraph.edit() as edit:
        # Create a knowledge graph for LLM context
        context = edit.new_node(node_data={"type": "context", 
                                         "value": "user query"})
        entity = edit.new_node(node_data={"type": "entity", 
                                        "value": "named entity"})
        relation = edit.new_edge(from_node_id=context.node_id,
                                to_node_id=entity.node_id,
                                edge_data={"type": "contains"})
        
        # Verify the knowledge graph
        assert context.node_data.value == "user query"
        assert entity.node_data.value == "named entity"
        assert relation.edge_data.type == "contains"
```

### Semantic Web Applications

```python
def test_semantic_web():
    from mgraph_db.mgraph.MGraph import MGraph
    
    mgraph = MGraph()
    with mgraph.edit() as edit:
        # Create RDF-style triples
        subject = edit.new_node(node_data={"uri": "http://example.org/subject"})
        object = edit.new_node(node_data={"uri": "http://example.org/object"})
        predicate = edit.new_edge(from_node_id=subject.node_id,
                                 to_node_id=object.node_id,
                                 edge_data={"predicate": "relates_to"})
        
        # Verify triple structure
        assert subject.node_data.uri == "http://example.org/subject"
        assert object.node_data.uri == "http://example.org/object"
        assert predicate.edge_data.predicate == "relates_to"
```

## Advanced Usage

### Type-Safe Operations

```python
def test_type_safe_operations():
    from mgraph_db.mgraph.MGraph import MGraph
    from mgraph_db.mgraph.schemas.Schema__MGraph__Node import Schema__MGraph__Node
    from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data
    
    # Custom node data with runtime type checking
    class Custom_Node_Data(Schema__MGraph__Node__Data):
        name: str
        value: int
        priority: float
    
    # Type-safe node definition
    class Custom_Node(Schema__MGraph__Node):
        node_data: Custom_Node_Data
    
    mgraph = MGraph()
    with mgraph.edit() as edit:
        # Create typed node
        node = edit.new_node(node_type=Custom_Node,
                            name="test",
                            value=42,
                            priority=1.5)
        
        # Verify type safety
        assert node.node_data.name == "test"
        assert node.node_data.value == 42
        assert node.node_data.priority == 1.5
        
        # Demonstrate type-safe processing
        result = node.node_data.priority * 2.0
        assert result == 3.0
```

### Using the Index System

```python
def test_index_system():
    from mgraph_db.mgraph.MGraph import MGraph
    
    mgraph = MGraph()
    with mgraph.edit() as edit:
        # Create nodes
        node1 = edit.new_node(node_type=Custom_Node,
                             name="test",
                             value=42,
                             priority=1.5)
        
        # Access index
        with edit.index() as index:
            # Get nodes by type
            nodes = index.get_nodes_by_type(Custom_Node)
            assert len(nodes) == 1
            
            # Get by relationship
            nodes_by_type = index.get_nodes_by_type(Custom_Node)
            assert node1.node_id in nodes_by_type
```

### Graph Export and Visualization

```python
def test_export_and_visualization():
    from mgraph_db.mgraph.MGraph import MGraph
    import os
    
    mgraph = MGraph()
    with mgraph.edit() as edit:
        # Create sample graph
        node1 = edit.new_node()
        node2 = edit.new_node()
        edge = edit.new_edge(from_node_id=node1.node_id,
                            to_node_id=node2.node_id)
    
    # Test various export formats
    with mgraph.export() as export:
        # DOT format
        dot = export.to__dot()
        assert 'digraph' in dot
        
        # Mermaid format
        mermaid = export.to__mermaid()
        assert 'graph TD' in mermaid
        
        # GraphML format
        graphml = export.to__graphml()
        assert 'graphml' in graphml
        
        # RDF/Turtle format
        turtle = export.to__turtle()
        assert '@prefix' in turtle
    
    # Test visualization
    output_file = 'test_graph.png'
    with mgraph.screenshot() as screenshot:
        screenshot.save_to(output_file)
        assert os.path.exists(output_file)
        if os.path.exists(output_file):
            os.remove(output_file)
```

## Installation

```bash
pip install mgraph-db
```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/your-org/mgraph.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python -m pytest tests/`)
5. Submit a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.