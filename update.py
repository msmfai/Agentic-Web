#!/usr/bin/env python3
"""
# Repository Update Workflow

**File Tags**: #type/code-file
**Inheritable Tags**: #domain/automation #layer/infrastructure #category/orchestration

## Purpose
Simple orchestrator that runs repository maintenance scripts in sequence.

This is a pure container - all actual logic lives in the individual scripts.

Workflow:
1. [[add_location_tags.py]] - Add location tags to Python files
2. [[generate_ast.py]] - Generate AST cache from Python source
3. [[generate_tags.py]] - Generate tag indices (repository-map, tag-index)
4. [[graph_metrics.py]] - Analyze knowledge graph health
5. [[janitor.py]] - Run repository health checks

Usage:
    python update.py
    uv run update.py
"""

import subprocess
import sys
from pathlib import Path

# Workflow: list of (script_name, is_critical)
# Critical scripts stop the workflow on failure
# Non-critical scripts continue even if they fail
WORKFLOW = [
    ("add_location_tags.py", True),
    ("generate_ast.py", True),
    ("generate_tags.py", True),
    ("graph_metrics.py", False),  # Metrics are informational
    ("janitor.py", True),
]


def main():
    """Run all maintenance scripts in sequence."""
    root = Path(__file__).parent

    for script, is_critical in WORKFLOW:
        try:
            subprocess.run(["uv", "run", script], check=True, cwd=root)
        except subprocess.CalledProcessError:
            if is_critical:
                print(f"\n{script} failed (critical). Stopping workflow.")
                sys.exit(1)
            else:
                print(f"\n{script} failed (non-critical). Continuing...")


if __name__ == "__main__":
    main()
