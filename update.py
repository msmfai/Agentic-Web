#!/usr/bin/env python3
"""
# Repository Update Workflow

**File Tags**: #type/code-file
**Inheritable Tags**: #domain/automation #layer/infrastructure #category/orchestration

## Purpose
Simple orchestrator that runs repository maintenance scripts in sequence.

This is a pure container - all actual logic lives in the individual scripts.

Workflow:
1. [[maintenance_scripts/add_location_tags.py]] - Add location tags to Python files
2. [[maintenance_scripts/generate_ast.py]] - Generate AST cache from Python source
3. [[maintenance_scripts/generate_tags.py]] - Generate tag indices (repository-map, tag-index)
4. [[maintenance_scripts/graph_metrics.py]] - Analyze knowledge graph health
5. [[maintenance_scripts/janitor.py]] - Run repository health checks

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
    ("maintenance_scripts/add_location_tags.py", True),
    ("maintenance_scripts/generate_ast.py", True),
    ("maintenance_scripts/generate_tags.py", True),
    ("maintenance_scripts/graph_metrics.py", False),  # Metrics are informational
    ("maintenance_scripts/janitor.py", True),
]


def main():
    """Run all maintenance scripts in sequence."""
    root = Path(__file__).parent

    for script, is_critical in WORKFLOW:
        script_path = root / script
        try:
            subprocess.run([sys.executable, str(script_path)], check=True, cwd=root)
        except subprocess.CalledProcessError:
            if is_critical:
                print(f"\n{script} failed (critical). Stopping workflow.")
                sys.exit(1)
            else:
                print(f"\n{script} failed (non-critical). Continuing...")


if __name__ == "__main__":
    main()
