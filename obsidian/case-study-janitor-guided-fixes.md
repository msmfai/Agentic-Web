---
tags:
  - type/case-study
  - domain/automation
  - category/validation
---

# Case Study: Janitor-Guided Repository Fixes

**Date**: 2025-10-20
**Outcome**: Successful automated validation and AI-guided fixes

## Problem

After implementing a custom AST cache system and Obsidian integration, the repository had inconsistent YAML frontmatter formatting across 21 files. Tags were using inline array format `[tag1, tag2]` instead of YAML list format, which caused Obsidian to not properly recognize hierarchical tags with slashes (like `type/concept`, `domain/mathematics`).

**Challenge**: Manually fixing 21 files across different directories would be error-prone and time-consuming. The system needed to be maintainable by AI agents without full context.

## Solution: Deterministic Janitor + AI Execution

### Phase 1: Janitor Detection

The [[janitor.py]] validation system was enhanced to:

1. **Parse both tag formats** (inline array and YAML list)
2. **Flag inline format as warning** with clear explanation
3. **Generate individual issue files** in `whiteboard/janitor/` for each problem
4. **Provide actionable context** with before/after examples

**Janitor Output**:
```
21 WARNING(S) FOUND:
  - 10 AST cache files
  - 3 Python code files
  - 3 root documentation files
  - 5 obsidian concept/pattern files
```

### Phase 2: Issue File Structure

Each issue file contained:

```markdown
---
tags: [janitor-issue, janitor-issue/tag-format-warning, severity/warning]
---

# Issue #1: calculator.py

**File**: [[code\calculator.py|calculator.py]]
**Severity**: WARNING

## Problem
Tags use inline array format [tag1, tag2]. Obsidian prefers YAML list format

## Context

**What's wrong**: Inline array format
**What's expected**: YAML list format with examples
**Why**: Obsidian compatibility for hierarchical tags
**How to fix**: Step-by-step conversion example
```

### Phase 3: Systematic Fixes

**Strategy**: Fix issues one at a time, delete issue file after completion.

1. **Fixed generate_ast.py first** (root cause for 10 files)
   - Updated tag generation to use YAML list format
   - Regenerated AST cache → 10 files fixed automatically

2. **Fixed remaining 11 files manually** following janitor instructions:
   - Converted inline `tags: [type/concept, domain/math]`
   - To YAML list format:
     ```yaml
     tags:
       - type/concept
       - domain/math
     ```
   - Deleted corresponding issue file after each fix

3. **Re-ran janitor** to verify completion

## Results

### Metrics

| Metric | Value |
|--------|-------|
| Initial warnings | 21 |
| Files fixed automatically | 10 (via generate_ast.py) |
| Files fixed manually | 11 |
| Final warnings | 0 |
| Time to complete | ~5 minutes |
| Human errors | 0 |

### Key Success Factors

**1. Deterministic Validation**
- Janitor scanned entire repository in 3 phases
- Collected all block markers globally
- Validated cross-references between files
- No ambiguity in what's wrong

**2. Contextual Instructions**
- Each issue file explained the "why" not just "what"
- Included before/after examples
- Referenced Obsidian compatibility requirements
- AI could fix without understanding entire system

**3. Feedback Loop**
- Fix one file → delete issue → re-run janitor
- Immediate verification of each fix
- No batch changes that might introduce new issues

**4. Root Cause Fixing**
- Identified generate_ast.py as source of 10 issues
- Fixed generator → all future AST files use correct format
- Prevented issue from recurring

## Technical Details

### Janitor Enhancements Made

```python
# Parse both tag formats
tags_match_inline = re.search(r'tags:\s*\[(.*?)\]', yaml_content)
tags_match_list = re.search(r'tags:\s*\n((?:\s+-\s+.+\n?)+)', yaml_content)

# Track format for validation
frontmatter['_tag_format'] = 'inline' or 'yaml-list'

# Warn on inline format
if frontmatter.get('_tag_format') == 'inline':
    self.issues.append(Issue(
        severity='warning',
        message="Tags use inline array format. Obsidian prefers YAML list"
    ))
```

### Issue Classification

New issue type added:
- Tag: `janitor-issue/tag-format-warning`
- Severity: `warning` (not breaking, but suboptimal)
- Context: Comprehensive explanation with examples

## Lessons Learned

### What Worked

1. **Individual issue files** > single report
   - Each file focused on one problem
   - Could be deleted as confirmation of fix
   - Natural checklist for AI agent

2. **Prescriptive context** without being restrictive
   - Explained "what's wrong" and "what's expected"
   - Showed examples but didn't dictate implementation
   - AI could adapt to edge cases

3. **Hierarchical validation**
   - Fix generate_ast.py first (upstream)
   - Then fix existing files (downstream)
   - Prevented rework

### What Could Be Improved

1. **Auto-fix capability**: Janitor could fix tag format automatically
2. **Batch operations**: Group similar fixes for efficiency
3. **Priority ordering**: Fix upstream issues before downstream

## Conclusion

**The system works as designed**: A deterministic janitor can guide an AI agent through complex repository maintenance without requiring full context. The janitor acts as a "diagnostician" and the AI as an "executor" following clear instructions.

**Key Insight**: You cannot expect humans (or AI with limited context) to maintain complex systems manually. Deterministic validation + clear instructions + feedback loops = maintainable knowledge graph.

## Related

- [[janitor.py|Janitor Implementation]]
- [[generate_ast.py|AST Generator]]
- [[python-superset-design.md|Python Superset Design]]
- [[ast-cache-system.md|AST Cache System]]

## Tags Explanation

- `type/case-study`: Real-world example of system usage
- `domain/automation`: Automated validation and fixes
- `category/validation`: Repository health checking
