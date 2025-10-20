---
tags:
  - type/index
---

# Obsidian Knowledge Graph Demonstration

This repository demonstrates a **unified code-documentation system** using Obsidian as a knowledge graph.

## Quick Start

- **For Claude Code**: See [[CLAUDE.md]] for complete repository instructions
- **For humans**: See [[index/repository-map|Repository Map]] for a high-level snapshot of the codebase

## Key Features

- Code and documentation interconnected through bidirectional wikilinks
- Tag-based navigation and organization
- AST cache for searchable code representations
- Automated health checks via [[janitor.py]]
- Graph metrics tracking via [[graph_metrics.py]]

## Running the Demo

```bash
# Run the calculator
cd code
python main.py

# Check repository health
uv run janitor.py

# Update all indices and metrics
uv run update.py
```

## Philosophy

This system treats code as a knowledge graph node, not just text. See [[CLAUDE.md#Philosophy]] for the complete philosophy.
