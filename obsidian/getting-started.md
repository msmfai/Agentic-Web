---
tags:
  - type/guide
  - type/entry-point
  - purpose/onboarding
  - category/tutorial
audience: new users, beginners
---

# Getting Started with the Knowledge Graph

Your first steps exploring code as an interconnected graph

This guide will help you set up Obsidian and start navigating this repository as a knowledge graph.

## Prerequisites

- [Obsidian](https://obsidian.md/) installed on your system (free)
- This repository cloned locally
- (Optional) Python 3.11+ with `uv` for running the calculator

## Step 1: Open the Vault

1. Launch Obsidian
2. Click "Open folder as vault"
3. Navigate to this repository's root folder: `d:\dev\obsidian_idea_demonstration`
4. Click "Open"

Obsidian will now index all `.md` files in the vault.

## Step 2: Install Custom File Extensions Plugin

To make `.py` files participate in the graph, you need the Custom File Extensions plugin:

1. Open Settings (gear icon, bottom left)
2. Navigate to **Community plugins**
3. Click **Browse** and search for "Custom File Extensions"
4. Click **Install**, then **Enable**
5. Go to the plugin's settings (under Community Plugins)
6. Click **Add New Extension**
7. Enter `py` as the extension
8. Set view type to **Markdown**
9. Click **Add**
10. Restart Obsidian

Now `.py` files will appear as graph nodes with clickable wikilinks!

## Step 3: Explore the Graph

### Open Graph View

- Click the graph icon in the left sidebar (looks like connected nodes)
- You'll see all files as nodes, connected by wikilinks

### Try These Filters

Use the filter box at the top of Graph View:

```text
tag:#type/code-file
```

Shows only Python code files

```text
tag:#domain/mathematics
```

Shows all math-related files

```text
tag:#pattern/strategy
```

Shows files implementing the Strategy Pattern

```text
path:obsidian/
```

Shows only documentation files

### Navigate the Graph

- **Click any node** to open that file
- **Hover over a node** to see its connections highlighted
- **Use mouse wheel** to zoom in/out
- **Drag nodes** to rearrange the visualization
- **Right-click** for more options

## Step 4: Follow Your First Link Trail

Let's trace a concept from documentation → implementation:

1. Open [[arithmetic-operations|Arithmetic Operations]] (concept doc)
2. Click the link to `[[../code/operations.py|Operations Module]]`
3. You're now viewing the Python code
4. Scroll through the docstring to see links back to concepts
5. Notice the `#domain/mathematics` and `#layer/core` tags
6. Use Obsidian's "Backlinks" pane (right sidebar) to see what else links here

You just navigated from "what" → "how" → "why" using the graph!

## Step 5: Search by Tags

Tags are the primary organizational system:

1. Open the tag pane (left sidebar, tag icon)
2. Click on any tag to see all files with that tag
3. Common tags to explore:
   - `#domain/mathematics` - All math-related code
   - `#layer/interface` - User-facing interface code
   - `#pattern/strategy` - Strategy pattern usage
   - `#type/concept` - Conceptual documentation

## Step 6: Try the Calculator

To see the code in action:

```bash
cd code
python main.py
```

Interactive session:

```text
> add 5 3
Result: 8.0

> sin 90
Result: 1.0

> divide 10 2
Result: 5.0

> quit
```

As you use the calculator, you can explore the code that powers each operation through the graph.

## Step 7: Explore AST Cache

The `ast-cache/` folder contains auto-generated markdown files representing every Python function and class:

1. Navigate to `ast-cache/code/calculator/` in Obsidian
2. Open `Calculator.ast.md` (the Calculator class)
3. You'll see the signature, docstring, and source code
4. These files inherit all tags from their source Python files
5. Use them for tag-based searches (Python file tags aren't indexed by Obsidian)

**Pro tip**: Search for `#domain/mathematics` in Obsidian - you'll find AST cache files, not Python files. This is by design!

## Common Workflows

### "Show me all validation code"

1. Search tags for `#domain/validation` OR
2. Use global search (Cmd/Ctrl + Shift + F) for `#domain/validation`
3. Results show AST cache files and docs
4. Click through to explore

### "What design patterns are used?"

1. Check [[../index/repository-map|Repository Map]] → "Implemented Patterns" section
2. Or search tags for `#pattern/`
3. Click pattern docs like [[strategy-pattern|Strategy Pattern]] to learn more

### "Where is this function called?"

1. Open the function's AST cache file (e.g., `ast-cache/code/operations/add.ast.md`)
2. Check the Backlinks pane (right sidebar)
3. See all references across code and docs

### "Understand the architecture"

1. Start with [[architecture-overview|Architecture Overview]]
2. Follow links to layer descriptions
3. Explore tagged files in each layer
4. Trace execution from entry-point → interface → domain → core

## Advanced Features

### Local Graph View

- Open any file
- Click the local graph icon (small graph icon in file header)
- See only nodes directly connected to this file
- Great for focused exploration

### Search Operators

```text
tag:#domain/mathematics AND path:code/
```

Math code files only

```text
tag:#layer/core OR tag:#layer/domain
```

Core and domain layer files

```text
line:(Strategy Pattern) tag:#type/code-file
```

Code files mentioning "Strategy Pattern"

### Customize Graph Colors

1. Open Graph View Settings
2. Under "Groups", add filters like `tag:#domain/mathematics`
3. Assign colors to different groups
4. Now domains appear in different colors!

## Troubleshooting

### Python files don't show up in graph

- Did you install Custom File Extensions plugin?
- Did you add `py` extension with Markdown view type?
- Did you restart Obsidian after configuring?

### Wikilinks in Python files don't work

- Wikilinks in `.py` files only work after Custom File Extensions plugin is installed
- Make sure `.py` is set to "Markdown" view type

### Tags from Python files don't appear in search

- This is expected! Obsidian doesn't index tags from `.py` files
- Use AST cache files instead - they inherit all source file tags
- See [[tag-inheritance|Tag Inheritance]] for details

### AST cache is out of date

```bash
python maintenance_scripts/generate_ast.py
```

## Next Steps

Now that you're oriented:

- **Understand the architecture**: [[architecture-overview|Architecture Overview]]
- **See project status**: [[../index/repository-map|Repository Map]]
- **Learn about tags**: [[tag-inheritance|Tag Inheritance]]
- **Read a case study**: [[case-study-janitor-guided-fixes|Janitor-Guided Fixes]]
- **Explore graph metrics**: [[graph-metrics-system|Graph Metrics]]

## Resources

- [Obsidian Documentation](https://help.obsidian.md/)
- [Custom File Extensions Plugin](https://github.com/MeepTech/obsidian-custom-file-extensions-plugin)
- [[README.md|Repository README]]
- [[../CLAUDE.md|LLM Instructions]] (for understanding how Claude Code uses this system)

---

**Happy exploring!** The graph grows richer the more you follow links and discover connections.
