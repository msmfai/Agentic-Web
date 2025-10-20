---
tags:
  - type/index
  - type/entry-point
  - purpose/human-entry-point
audience: developers, users, contributors
---

# Code as Knowledge Graph

> A living codebase you can explore like Wikipedia

## 🤖 How This Was Built

**This entire repository was created using only Claude Code - no manual editing.** Every file, every tag, every link was generated through AI-assisted development to demonstrate what's possible when you let an AI agent manage a knowledge graph system end-to-end.

This approach ensures perfect consistency with tag schemas, automated validation workflows, and interconnected documentation - because the same AI that understands the system also maintains it.

---

This repository shows what happens when you stop treating code and documentation as separate artifacts and instead merge them into a single, navigable knowledge graph.

Instead of jumping between code files, API docs, architecture diagrams, and design documents, you navigate directly from "what does this do?" to "why was it built this way?" to "how is it implemented?" - all through clickable links in a visual graph.

## What is This?

This is a simple calculator application, but organized in a fundamentally different way:

- **Code files are graph nodes** - Python files participate directly in Obsidian's knowledge graph
- **Documentation lives alongside code** - Concepts, patterns, and architecture decisions are linked bidirectionally
- **Tags replace folder hierarchies** - Organization emerges from tags like `#domain/mathematics`, `#layer/core`, `#pattern/strategy`
- **Navigation follows meaning** - Move from "why we made this choice" to "how it's implemented" to "what the code does"

The result: you can explore this codebase like a web of interconnected ideas rather than a tree of folders.

## Quick Start

### Option 1: Set Up Obsidian (Recommended)

To experience the full knowledge graph with visual navigation:

1. **Install Obsidian** - Download from [obsidian.md](https://obsidian.md/) (free)

2. **Open this folder as a vault**
   - Launch Obsidian
   - Click "Open folder as vault"
   - Select this repository folder
   - Click "Open"

3. **Install the Custom File Extensions Plugin**
   - Open Settings (⚙️ icon, bottom left)
   - Navigate to **Community plugins**
   - Turn off "Restricted mode" if prompted
   - Click **Browse**
   - Search for "Custom File Extensions"
   - Click **Install**, then **Enable**
   - In plugin settings, click **Add New Extension**
   - Enter `py` as the extension
   - Set view type to **Markdown**
   - Click **Add**
   - **Restart Obsidian**

4. **Start Exploring**
   - Open Graph View (graph icon in left sidebar)
   - Try these starting points:
     - [[obsidian/getting-started|Getting Started Guide]] - Detailed tutorial and workflows
     - [[obsidian/architecture-overview|Architecture Overview]] - How this system works
     - [[index/repository-map|Repository Map]] - What's in this repository
     - [[code/main.py|main.py]] - Entry point to the calculator code
   - Try graph filters like `tag:` followed by `#domain/mathematics` or `#type/code-file`

### Option 2: Browse as Markdown Files

Not ready to install Obsidian? You can still read everything as regular markdown:

- **Getting Started**: Open `obsidian/getting-started.md` in any text editor
- **Architecture**: See `obsidian/architecture-overview.md` for how this works
- **Repository Map**: Check `index/repository-map.md` for what's inside
- **For AI Agents**: Read `CLAUDE.md` for LLM instructions

You'll miss the visual graph and clickable links, but all documentation is fully readable as plain text.

## Try the Calculator

Want to see the code in action first?

```bash
cd code
python main.py
```

Example session:

```text
> add 5 3
Result: 8.0

> sin 90
Result: 1.0

> divide 10 2
Result: 5.0

> quit
```

Then open the graph to explore how each operation is implemented!

## The Big Idea

Traditional codebases separate code from context:

```text
code/             docs/              Your Brain
├─ foo.py         ├─ architecture/   ├─ Why did we...?
├─ bar.py         ├─ patterns/       ├─ What depends on...?
└─ baz.py         └─ decisions/      └─ Where should I...?
```

This system unifies them:

```text
Knowledge Graph
├─ foo.py ←→ "Strategy Pattern" ←→ "Why we chose delegation"
├─ bar.py ←→ "Input Validation" ←→ "User safety requirements"
└─ baz.py ←→ "Trigonometry" ←→ "Mathematical domain"
```

Every piece of code is connected to its rationale, every pattern to its usage, every decision to its consequences.

## What's Inside

This demonstration contains:

- **12 Python files** - A working calculator with trig, arithmetic, and validation
- **8 documentation files** - Concepts, patterns, guides, and case studies
- **110+ AST cache nodes** - Auto-generated searchable representations of every function/class
- **3 auto-generated indices** - Repository map, tag index, and metrics

All interconnected through wikilinks. All navigable as a knowledge graph.

## Key Features

### Bidirectional Links

- Code links to concepts that explain it
- Concepts link back to implementations
- Navigate in any direction

### Tag-Based Organization

- Domain tags - What area? (mathematics, ui, testing, automation)
- Layer tags - What level? (entry-point, interface, domain, core)
- Pattern tags - What approach? (strategy, delegation, function-registry)

### Automated Maintenance

- AST generation keeps code representations fresh
- Tag indices auto-update when structure changes
- Health checks validate consistency
- Graph metrics track system evolution

### Tool Support

```bash
uv run update.py      # Complete update workflow (runs all the tools below):
                      #   - add_location_tags.py (Location tags for Python files)
                      #   - generate_ast.py (AST cache from Python files)
                      #   - generate_tags.py (Repository map + tag index)
                      #   - graph_metrics.py (Graph statistics)
                      #   - janitor.py (Health check + validation)
```

Individual tools (usually not needed - use `update.py` instead):

```bash
python maintenance_scripts/janitor.py --fix  # Fix issues with confirmation prompts
python maintenance_scripts/generate_ast.py   # Regenerate AST cache only
```

## Learn More

- **Philosophy**: Why unify code and docs? See [[CLAUDE#Philosophy|CLAUDE.md Philosophy section]]
- **Tag System**: How tags work in detail → [[obsidian/tag-inheritance|Tag Inheritance]]
- **Real Example**: See a complete workflow → [[obsidian/case-study-janitor-guided-fixes|Case Study: Janitor-Guided Fixes]]
- **Graph Metrics**: How we measure the graph → [[obsidian/graph-metrics-system|Graph Metrics System]]

## Status

This is a **demonstration project** showing what's possible when you treat your codebase as a knowledge graph. The calculator is intentionally simple - the interesting part is the organizational system around it.

**Current scale**: 12 Python files, 110+ graph nodes, 6 domains, 6 layers, 3 pattern families

**Maintained by**: Automated tooling + human curation
