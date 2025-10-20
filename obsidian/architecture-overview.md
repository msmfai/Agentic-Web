---
tags:
  - type/guide
  - purpose/architecture
  - category/reference
---

# Architecture Overview

How this knowledge graph system is organized

This document explains the architectural patterns, organizational principles, and design decisions that structure this repository.

## Architectural Principles

### 1. Code as Graph Nodes

Traditional approach: Code is text in files, documentation is separate

This system: Code files participate directly in the knowledge graph as first-class nodes with bidirectional links to concepts, patterns, and other code.

**Implementation**: Obsidian's Custom File Extensions plugin treats `.py` files as markdown, enabling wikilinks in docstrings.

### 2. Tags Over Folders

Traditional approach: Organization through nested directories (`src/domain/math/trig/`)

This system: Flat file structure with hierarchical tags (`#domain/mathematics/trigonometry`)

**Why**: Multiple orthogonal views of the same content. A file can be `#domain/mathematics`, `#layer/core`, and `#pattern/strategy` simultaneously.

### 3. Documentation Lives With Context

Traditional approach: API docs auto-generated, architecture docs in `/docs`, design rationale lost

This system: Concepts and patterns documented explicitly, linked bidirectionally to implementations

**Result**: Navigate from "why we made this choice" → "what pattern we used" → "how it's implemented"

## Tag System Architecture

Tags provide multiple organizational dimensions:

### Domain Tags (`#domain/*`)

What area of functionality?

- `#domain/mathematics` - Mathematical operations (trig, arithmetic)
- `#domain/ui` - User interface and interaction
- `#domain/testing` - Test suites and validation
- `#domain/automation` - Repository maintenance tools

**Granularity**: Can be hierarchical


- `#domain/mathematics/trigonometry` - Specific subdomain
- `#domain/testing/unit` vs `#domain/testing/integration`

See [[../index/repository-map|Repository Map]] for current domains.

### Layer Tags (`#layer/*`)

What level of abstraction?

- `#layer/entry-point` - Application entry points (main.py)
- `#layer/interface` - User-facing interfaces (Calculator class)
- `#layer/domain` - Business logic (operation implementations)
- `#layer/core` - Low-level utilities and primitives
- `#layer/test` - Test infrastructure

**Dependency Flow**: entry-point → interface → domain → core

**Rule**: Higher layers depend on lower layers, never the reverse

### Pattern Tags (`#pattern/*`)

What design approach is used?

- `#pattern/strategy` - Strategy pattern family
- `#pattern/strategy/delegation` - Calculator delegates to operations
- `#pattern/strategy/function-registry` - Operations registered by name

**Purpose**: Connect code to architectural decisions and document rationale

### Type Tags (`#type/*`)

What kind of file is this?

- `#type/code-file` - Python source
- `#type/concept` - Conceptual documentation
- `#type/pattern` - Design pattern description
- `#type/guide` - Tutorial/how-to
- `#type/index` - Auto-generated index

**Purpose**: Enable filtering in graph view and searches

### Purpose Tags (`#purpose/*`)

Why does this file exist?

- `#purpose/implementation` - Executable code
- `#purpose/documentation` - Human understanding
- `#purpose/llm-instructions` - AI agent guidance
- `#purpose/onboarding` - New user orientation

**Purpose**: Clarify intent and audience

## Directory Structure

### Minimal Physical Organization

```text
obsidian_idea_demonstration/
├── code/                    # Python source files
│   ├── main.py              # Entry point
│   ├── calculator.py        # Calculator class
│   └── operations.py        # Operation implementations
├── obsidian/                # Documentation (flat, no subdirs)
│   ├── arithmetic-operations.md
│   ├── calculator-interface.md
│   └── strategy-pattern.md
├── ast-cache/               # Auto-generated AST representations
│   └── code/
│       ├── calculator/
│       └── operations/
├── index/                   # Auto-generated indices
│   ├── repository-map.md
│   └── tag-index.md
├── README.md                # Human entry point
├── CLAUDE.md                # LLM entry point
└── schema.yaml              # Frontmatter schemas
```

**Key principle**: Physical structure is minimal. Logical organization comes from tags and links.

### Why Flat Documentation?

The `obsidian/` folder has no subdirectories by design:

- **Simpler paths**: `[[calculator-interface]]` vs `[[concepts/domain/calculator-interface]]`
- **No premature categorization**: Don't force a single hierarchy
- **Tag-based discovery**: Use `#type/concept` + `#domain/mathematics` instead of `/concepts/math/`
- **Easier refactoring**: Rename files without breaking nested path references

## AST Cache Architecture

### Purpose

Python file tags aren't indexed by Obsidian (plugin limitation). AST cache files are auto-generated markdown representations that:

1. **Inherit all source file tags**
2. **Are fully searchable** in Obsidian
3. **Provide detailed code structure** (signatures, docstrings, source)
4. **Enable tag-based discovery** of functions/classes

### Structure

For each Python file, we generate AST nodes:

```text
code/calculator.py
  → ast-cache/code/calculator/Calculator.ast.md (class)
  → ast-cache/code/calculator/Calculator.calculate.ast.md (method)
  → ast-cache/code/calculator/Calculator.run_interactive.ast.md (method)
```

Each AST file contains:

- **Full tag inheritance** from source file
- **Node signature** (function/class definition)
- **Docstring** (if present)
- **Source code** (full implementation)

### Tag Inheritance Limitation

**Critical**: AST files inherit ALL module-level tags. This means:

- Every function in a module gets the same tags
- Cannot tag individual functions differently
- Use specific subdomain tags (like `#domain/mathematics/trigonometry`) ONLY on focused modules
- Mixed-concern modules should use broad tags (`#domain/mathematics` + `#category/mixed-concerns`)

See [[tag-inheritance|Tag Inheritance]] for complete details.

### Generation

```bash
python maintenance_scripts/generate_ast.py
```

Run this after modifying Python files or changing tags.

## Wikilink Architecture

### Path-Based Links

Use relative paths to avoid filename conflicts:

From Python files in `code/`:

```python
"""
Related: [[../obsidian/arithmetic-operations|Arithmetic Operations]]
Dependencies: [[calculator.py|Calculator Class]]  # Same directory
"""
```

From markdown files in `obsidian/`:

```markdown
Implementation: [[../code/operations.py|Operations Module]]
Related: [[calculator-interface|Calculator Interface]]  # Same directory
```

**Why**: Allows duplicate filenames in different folders, makes refactoring easier

### Link Types

**Concept links**: Code → conceptual documentation

```python
"""Implements [[../obsidian/arithmetic-operations|basic arithmetic operations]]."""
```

**Pattern links**: Code → design pattern rationale

```python
"""Uses [[../obsidian/strategy-pattern|Strategy Pattern]] for operation dispatch."""
```

**Implementation links**: Concept → code

```markdown
See implementation in [[../code/operations.py#add|add function]]
```

**Cross-reference links**: Between related documentation

```markdown
Related: [[single-responsibility|Single Responsibility Principle]]
```

## Index Architecture

### Auto-Generated Indices

Two main indices in `index/`:

1. **[[../index/repository-map|Repository Map]]** - High-level project state
   - File counts by type
   - Active domains, layers, patterns
   - Tag summaries with file lists

2. **[[../index/tag-index|Tag Index]]** - Complete tag inventory
   - Every tag in the repository
   - All files with each tag
   - Embedded in graph via tag frontmatter

### Generation

```bash
python maintenance_scripts/generate_tags.py
```

Run after adding/removing files or changing tags.

## Health Check Architecture

The janitor (`janitor.py`) validates repository consistency:

### Validation Schema

Based on [[../schema.yaml|schema.yaml]]:

- **Python files**: Must have H1 header, inline hashtags, `#type/code-file` tag
- **Markdown files**: Must have YAML frontmatter with required tags
- **AST cache**: Must be up-to-date with source files
- **File placement**: Code in `code/`, docs in `obsidian/`, etc.

### Auto-Fix Capabilities

```bash
python maintenance_scripts/janitor.py --fix
```

Can automatically:

- Add missing tags
- Standardize frontmatter format
- Regenerate AST cache
- Fix common formatting issues

### Workflow Integration

**CRITICAL**: Always run health check before committing:

```bash
uv run update.py  # Regenerate AST + indices + check health
```

See [[case-study-janitor-guided-fixes|Case Study: Janitor-Guided Fixes]] for examples.

## Graph Metrics Architecture

The [[graph-metrics-system|Graph Metrics System]] tracks graph evolution:

### Metrics Collected

- **Node counts** by type (code, docs, AST)
- **Edge counts** (wikilinks)
- **Tag distribution** (most/least used)
- **Graph density** (connectivity)
- **Orphan detection** (unlinked nodes)
- **Tag coverage** (files with required tags)

### Generation

```bash
python maintenance_scripts/graph_metrics.py
```

Outputs JSON metrics for tracking over time.

## Implemented Design Patterns

### Strategy Pattern

**Where**: [[../code/calculator.py|Calculator]] delegates operations

**Why**: Extensible - add new operations without modifying calculator

**Implementation**: Function registry in [[../code/operations.py|operations.py]]

See [[strategy-pattern|Strategy Pattern]] for details.

### Single Responsibility

**Where**: Each operation is a separate function

**Why**: Testable, reusable, composable

**Implementation**: [[../code/operations.py|operations.py]] exports individual functions

See [[single-responsibility|Single Responsibility Principle]] for details.

### Registry Pattern

**Where**: Operations registered by name in `OPERATIONS` dict

**Why**: Dynamic dispatch, easy extensibility

**Implementation**: `OPERATIONS = {'add': add, 'subtract': subtract, ...}`

## Data Flow

### User Interaction Flow

```text
User Input
    ↓
main.py (#layer/entry-point)
    ↓
Calculator.run_interactive() (#layer/interface)
    ↓
Calculator.calculate() (#layer/interface)
    ↓
OPERATIONS[op_name](*args) (#layer/domain)
    ↓
Operation function (add/subtract/sin/etc) (#layer/core)
    ↓
Result returned back up the chain
```

### Tag-Based Discovery Flow

```text
User searches for #domain/mathematics
    ↓
Obsidian finds AST cache files (not Python files - limitation)
    ↓
User clicks ast-cache/code/operations/add.ast.md
    ↓
Sees source code, docstring, signature
    ↓
Follows wikilink to source: [[../../code/operations.py|operations.py]]
    ↓
Views actual Python file in graph
```

### Documentation Flow

```text
Concept documented (e.g., "Strategy Pattern")
    ↓
Pattern document links to implementations
    ↓
Code files link back to pattern document
    ↓
Bidirectional navigation enabled
    ↓
User can explore "why" and "how" in any direction
```

## Extension Points

### Adding New Code

1. Create `.py` file in `code/`
2. Add module docstring with:
   - H1 header
   - Inline hashtags (domain, layer, pattern)
   - `#type/code-file` tag
   - Wikilinks to related concepts
3. Run `uv run update.py`

See [[../CLAUDE.md#Adding New Code|Adding New Code in CLAUDE.md]]

### Adding New Documentation

1. Create `.md` file in `obsidian/` (flat structure)
2. Add YAML frontmatter with tags
3. Use wikilinks to connect to code and other docs
4. Run `uv run update.py`

See [[../CLAUDE.md#Adding New Documentation|Adding New Documentation in CLAUDE.md]]

### Adding New Domains

1. Choose domain name (e.g., `#domain/visualization`)
2. Tag relevant files with new domain
3. Optionally create concept document explaining the domain
4. Run `python maintenance_scripts/generate_tags.py` to update indices
5. New domain appears in [[../index/repository-map|Repository Map]]

### Adding New Patterns

1. Document pattern in `obsidian/pattern-name.md`
2. Tag with `#type/pattern` and `#pattern/pattern-name`
3. Tag implementing code with same pattern tag
4. Add wikilinks: pattern doc → implementations, code → pattern doc
5. Pattern appears in "Implemented Patterns" section of repository map

## Trade-offs and Limitations

### Current Limitations

**Python tag indexing**: Obsidian doesn't index tags in `.py` files

- **Workaround**: Use AST cache for tag-based discovery
- **Cost**: Extra generation step, duplicate information

**Manual tag maintenance**: Tags in Python must be inline hashtags

- **Reason**: YAML frontmatter can't be first line (Python requires `"""`)
- **Risk**: Easier to forget or mismatch tags
- **Mitigation**: Janitor validates and can auto-fix

**AST tag inheritance**: All functions in a module get same tags

- **Reason**: Tags are module-level, not function-level
- **Implication**: Can't tag individual functions differently
- **Workaround**: Keep modules focused on single domain

### Design Trade-offs

**Flat documentation structure**

- **Pro**: Simpler paths, no premature categorization
- **Con**: Harder to browse in file explorer (relies on Obsidian)

**Tag-based organization**

- **Pro**: Multiple orthogonal views, flexible reorganization
- **Con**: Requires discipline, tags can drift

**AST cache duplication**

- **Pro**: Full searchability, detailed code structure
- **Con**: Doubles repository size, needs regeneration

**Custom file extensions plugin dependency**

- **Pro**: Python files in graph, wikilinks in docstrings
- **Con**: Requires manual setup, not standard Obsidian

## Future Directions

Potential enhancements:

- **Automated graph metrics dashboard** - Track evolution over time
- **Link validation** - Detect broken wikilinks
- **Tag linting** - Enforce tag naming conventions
- **Multi-repo support** - Link across related repositories
- **Visual tag editor** - GUI for managing tags
- **Pattern detection** - Auto-suggest pattern tags from code analysis

## Learn More

- **Tag details**: [[tag-inheritance|Tag Inheritance]]
- **Current state**: [[../index/repository-map|Repository Map]]
- **All tags**: [[../index/tag-index|Tag Index]]
- **Validation**: [[case-study-janitor-guided-fixes|Janitor Case Study]]
- **Metrics**: [[graph-metrics-system|Graph Metrics System]]
- **Setup**: [[getting-started|Getting Started Guide]]

---

This architecture prioritizes **navigability over hierarchy**, **context over isolation**, and **discovery over structure**.
