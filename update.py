#!/usr/bin/env python3
"""
# Repository Update Workflow

**Tags**: #type/code-file #domain/automation #layer/infrastructure #category/orchestration

## Purpose
Run all repository maintenance tasks in the correct order.

This script runs:
1. Generate AST cache (from Python source files)
2. Generate tag indices (repository-map and tag-index)
3. Generate graph metrics (knowledge graph health analysis)
4. Run janitor health checks

Usage:
    python update.py
    uv run update.py
"""

import subprocess
import sys
from pathlib import Path


def run_command(description: str, command: list[str]) -> bool:
    """Run a command and return True if successful."""
    print()
    print("=" * 60)
    print(description)
    print("=" * 60)
    print()

    try:
        result = subprocess.run(command, check=True, cwd=Path(__file__).parent)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\nFAILED: {description}")
        print(f"Error: {e}")
        return False


def main():
    print()
    print("=" * 60)
    print("Repository Update & Validation")
    print("=" * 60)

    # Step 1: Generate AST cache
    if not run_command("Step 1: Generate AST Cache", ["uv", "run", "generate_ast.py"]):
        print("\nAST generation failed. Stopping.")
        sys.exit(1)

    # Step 2: Generate tag indices
    if not run_command("Step 2: Generate Tag Indices", ["uv", "run", "generate_tags.py"]):
        print("\nTag index generation failed. Stopping.")
        sys.exit(1)

    # Step 3: Generate graph metrics
    if not run_command("Step 3: Generate Graph Metrics", ["uv", "run", "graph_metrics.py"]):
        print("\nGraph metrics generation failed. Continuing anyway.")
        # Don't exit - metrics are informational, not blocking

    # Step 4: Run janitor health checks
    if not run_command("Step 4: Run Health Checks", ["uv", "run", "janitor.py"]):
        print("\nHealth checks failed. Repository may have issues.")
        sys.exit(1)

    # Success
    print()
    print("=" * 60)
    print("All tasks completed successfully!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
