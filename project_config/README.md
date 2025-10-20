---
tags:
  - type/guide
  - purpose/configuration
  - category/project-setup
---

# Project Configuration

This folder contains **your project-specific configuration**, separate from the scaffold framework.

## Files

### `tag_rules.yaml`

Define custom tags with **programmatically verifiable rules**:

- **Required properties**: Frontmatter fields that must exist
- **Property patterns**: Regex patterns property values must match
- **Link restrictions**: Which tags can link to files with this tag
- **Enforcement level**: `error`, `warning`, or `info`

## What the Janitor Can Verify

✅ **Property exists**: `required_properties: [status]` → checks frontmatter has `status` key
✅ **Property matches pattern**: `property_patterns: {status: "^(draft|published)$"}` → validates value
✅ **Link restrictions**: `allowed_inbound_tags: ["type/index"]` → only index files can link here
❌ **Content quality**: Cannot verify "is this well-written"
❌ **Semantic correctness**: Cannot verify "does this make sense"

## Example: Entry Point Tag

```yaml
entry-point:
  tag: "type/entry-point"

  required_properties:
    - audience       # Must exist in frontmatter

  link_restrictions:
    allowed_inbound_tags:
      - "type/entry-point"  # Only other entry points can link here
      - "type/index"        # Or index files

  enforcement: "error"
```

Files with `type/entry-point` must:

1. Have an `audience` property in frontmatter
2. Only be linked from other entry points or index files

## How It Works

1. **You define tags** in `tag_rules.yaml`
2. **Janitor validates** files programmatically
3. **Auto-fix available** for missing properties (adds `FIXME` placeholders)

```bash
python maintenance_scripts/janitor.py        # Check for violations
python maintenance_scripts/janitor.py --fix  # Auto-add missing properties
```

## Scaffold vs Project

- **Scaffold** (`schema.yaml`, `maintenance_scripts/`): Project-agnostic framework
- **Project** (`project_config/`): Your domain-specific rules

Keep your rules here so they're version-controlled with your project!
