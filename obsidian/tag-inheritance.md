---
tags:
  - type/concept
  - domain/automation
  - category/best-practices
  - category/code-generation
---

# Tag Inheritance in AST Cache

## Overview

AST cache files inherit ALL tags from their source Python file's module-level docstring. This creates both power and limitations.

## How It Works

When `generate_ast.py` creates AST cache files, it:

1. Extracts tags from the Python module's docstring (the custom `#hashtag` format)
2. Adds those tags to EVERY AST file generated from that module
3. Also adds AST-specific tags (`type/ast-node`, `ast-type/function`, etc.)

**Example:**

```python
# code/operations.py
"""
**Tags**: #domain/mathematics #pattern/strategy
"""

def add(a, b):  # ^add
    return a + b

def sin(x):  # ^sin
    return math.sin(x)
```

**Result:** Both `add.ast.md` AND `sin.ast.md` inherit:
- `#domain/mathematics`
- `#pattern/strategy`

## Why This Matters

### The Power

**Search across entire modules:**
- `#domain/mathematics` finds ALL functions in the operations module
- `#pattern/strategy` finds ALL strategy pattern implementations
- Enables "show me everything related to X" queries

**Automatic propagation:**
- Add a tag to the module → instantly applies to all functions
- Consistent tagging across related code
- No manual per-function tagging needed

### The Limitation

**Cannot tag individual functions differently:**

If a module contains mixed concerns (like `operations.py` with arithmetic, trigonometry, exponential functions), you CANNOT tag them separately at the function level.

**Bad approach:**
```python
"""
**Tags**: #domain/mathematics #domain/mathematics/trigonometry
"""
# ❌ Now sqrt(), factorial(), and other non-trig functions are tagged as trig!
```

**Good approach:**
```python
"""
**Tags**: #domain/mathematics #category/mixed-concerns
"""
# ✅ Broad tag acknowledges the module contains multiple subdomains
```

## Best Practices

### 1. Use Specific Tags Only for Focused Modules

✅ **Good - Focused module:**
```python
# test_calculator.py
"""
**Tags**: #domain/testing #domain/testing/integration
"""
# All tests in this file ARE integration tests
```

❌ **Bad - Mixed module:**
```python
# operations.py
"""
**Tags**: #domain/mathematics #domain/mathematics/trigonometry
"""
# Only SOME functions are trig - this is misleading!
```

### 2. Signal Mixed Concerns Explicitly

When a module intentionally contains multiple subdomains:

```python
"""
**Tags**: #domain/mathematics #category/mixed-concerns
"""
```

This tells users "this module contains multiple types of operations, tagged broadly."

### 3. Split Files for Granular Tags

If you need function-level tag granularity:

**Before:**
```
operations.py  #domain/mathematics
  - add()
  - sin()
  - sqrt()
  - log()
```

**After:**
```
arithmetic.py      #domain/mathematics/arithmetic
  - add()
  - subtract()

trigonometry.py    #domain/mathematics/trigonometry
  - sin()
  - cos()

exponential.py     #domain/mathematics/exponential
  - log()
  - exp()
```

## Why Not Function-Level Tags?

The current system uses Python docstring inline hashtags because:

1. **YAML frontmatter won't work** - Must be first line, but Python requires `"""`
2. **Inline hashtags** work but only at module level (the first docstring)
3. **Function docstrings** could theoretically use hashtags, but:
   - Would require new parsing logic
   - Obsidian doesn't index them (limitation of Custom File Extensions plugin)
   - Would complicate the inheritance model

## Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| **Module-level tags only** | Simple, consistent, automatic | Can't differentiate functions within a module |
| **Split into focused files** | Precise per-function tagging via file granularity | More files to manage, potential over-organization |
| **Mixed concerns tag** | Honest about module scope | Loses some search precision |

## Related

- Implementation: [[maintenance_scripts/generate_ast.py|AST Generator]]
- Tag system: [[CLAUDE.md#Tag System|CLAUDE.md Tag System]]
- Schema: [[schema.yaml|Schema Definition]]

## Gotchas for LLMs

**If you (Claude) are reading this:**

When you see a tag like `#domain/mathematics/trigonometry`:

1. ✅ **Check WHERE it's used** - Is it on a focused module or mixed module?
2. ❌ **Don't assume** every function in that module matches that specific subdomain
3. ✅ **Verify** by reading the actual source code if precision matters
4. ✅ **Remember** AST cache files inherit ALL parent tags, even if misleading

**Example of the gotcha:**

```
File: operations.py
Tags: #domain/mathematics #domain/mathematics/trigonometry

Function: sqrt()
Inherited tags: #domain/mathematics #domain/mathematics/trigonometry
Reality: sqrt is NOT trigonometry - it's a power operation!
```

**How to avoid:**
- Use broad tags for mixed modules
- Use specific tags only for focused modules
- Add `#category/mixed-concerns` to signal intentional breadth
