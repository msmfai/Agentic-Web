---
tags:
  - type/index
---

# Calculator Knowledge Graph

A calculator application organized as an Obsidian knowledge graph, where code files are integrated as nodes with bidirectional links to concepts and design patterns.

## Structure

### Code Files (#type/code-file)

- [[code/main.py|Main Entry Point]]
- [[code/calculator.py|Calculator Class]]
- [[code/operations.py|Operations Module]]

### Concepts

- [[concepts/calculator-interface|Calculator Interface]]
- [[concepts/arithmetic-operations|Arithmetic Operations]]
- [[concepts/user-input-validation|User Input Validation]]

### Design Patterns

- [[patterns/strategy-pattern|Strategy Pattern]]
- [[patterns/single-responsibility|Single Responsibility Principle]]

## Setup: Making .py Files Participate in the Graph

To make Python files appear in Obsidian's graph view, you need to install the **Custom File Extensions Plugin**:

1. Open Obsidian Settings → Community Plugins
2. Browse and search for "Custom File Extensions Plugin"
3. Install and enable the plugin
4. In the plugin settings, add `py` (and optionally `tex` or other extensions) to the list of extensions
5. Configure each extension to use the "Markdown" view type
6. Restart Obsidian

Once configured, `.py` files will be treated as markdown files, allowing:

- Wikilinks in comments to work and appear in the graph
- Files to show up as nodes in graph view
- Backlinks to function properly

**Plugin Repository**: [obsidian-custom-file-extensions-plugin](https://github.com/MeepTech/obsidian-custom-file-extensions-plugin)

## Running the Application

To run the calculator:

```bash
cd code
python main.py
```

## How This Works

Each code file includes:

- `#type/code-file` tag for filtering
- Documentation comments with Obsidian links to related concepts
- Links to design patterns used in the code
- Links to dependent/related code files

This creates a navigable knowledge graph where you can:

- Browse from concept → implementation
- Browse from code → understanding (concepts/patterns)
- See relationships between different parts of the system
- Explore design decisions and their rationale

## Graph Navigation Tips

- Use the Graph View in Obsidian to visualize relationships
- Filter by tags: `tag:#type/code-file`, `tag:#type/concept`, `tag:#type/pattern`
- Follow links in code comments to understand the "why" behind the code
- Backlinks show you what depends on each node
