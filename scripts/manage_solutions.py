#!/usr/bin/env python3
"""
Simple solution management for Celery workshop exercises.

Usage:
    python scripts/manage_solutions.py remove    # Remove solutions (create student version)
    python scripts/manage_solutions.py restore   # Restore solutions from backup
    python scripts/manage_solutions.py check     # Check current status
"""

import argparse
import re
import shutil
from pathlib import Path

# Files to process
EXERCISE_FILES = [
    "src/celery_workshop/chapter1_exercises.py",
    # Add more files here as needed
]

# Solution boundary patterns
START_PATTERN = re.compile(r"^\s*#\s*START\s+SOLUTION\s*$", re.IGNORECASE)
END_PATTERN = re.compile(r"^\s*#\s*END\s+SOLUTION\s*$", re.IGNORECASE)


def get_workspace_root() -> Path:
    """Get workspace root directory."""
    return Path(__file__).parent.parent


def find_solution_blocks(content: str) -> list[tuple[int, int]]:
    """Find all solution blocks in content."""
    lines = content.splitlines()
    blocks = []
    current_start = None

    for i, line in enumerate(lines):
        if START_PATTERN.match(line):
            current_start = i
        elif END_PATTERN.match(line) and current_start is not None:
            blocks.append((current_start, i))
            current_start = None

    return blocks


def remove_solutions(file_path: Path) -> None:
    """Remove solutions from a file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        blocks = find_solution_blocks(content)

        if not blocks:
            print(f"  No solutions found in {file_path.name}")
            return

        # Create backup
        backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
        shutil.copy2(file_path, backup_path)

        lines = content.splitlines()

        # Process blocks in reverse order
        for start_line, end_line in reversed(blocks):
            indent = " " * (len(lines[start_line]) - len(lines[start_line].lstrip()))
            placeholder = f"{indent}# TODO: Implement this function\n{indent}pass"
            lines[start_line:end_line + 1] = [placeholder]

        file_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  Removed {len(blocks)} solution(s) from {file_path.name}")

    except OSError as e:
        print(f"  Error processing {file_path.name}: {e}")


def restore_solutions(file_path: Path) -> None:
    """Restore solutions from backup."""
    backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")

    if not backup_path.exists():
        print(f"  No backup found for {file_path.name}")
        return

    try:
        shutil.copy2(backup_path, file_path)
        print(f"  Restored {file_path.name} from backup")
    except OSError as e:
        print(f"  Error restoring {file_path.name}: {e}")


def check_status(file_path: Path) -> None:
    """Check if file has solutions."""
    try:
        content = file_path.read_text(encoding="utf-8")
        blocks = find_solution_blocks(content)
        backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")

        if blocks:
            print(f"  {file_path.name}: has {len(blocks)} solution(s)")
        elif backup_path.exists():
            print(f"  {file_path.name}: no solutions (backup available)")
        else:
            print(f"  {file_path.name}: no solutions")

    except OSError as e:
        print(f"  {file_path.name}: error - {e}")


def process_files(action: str) -> None:
    """Process all exercise files with given action."""
    workspace = get_workspace_root()

    print(f"Processing exercise files in {workspace}")
    print("-" * 40)

    for file_pattern in EXERCISE_FILES:
        file_path = workspace / file_pattern
        if not file_path.exists():
            print(f"  Skipping {file_pattern} (not found)")
            continue

        if action == "remove":
            remove_solutions(file_path)
        elif action == "restore":
            restore_solutions(file_path)
        elif action == "check":
            check_status(file_path)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Manage exercise solutions",
        usage="python scripts/manage_solutions.py {remove|restore|check}"
    )
    parser.add_argument(
        "action",
        choices=["remove", "restore", "check"],
        help="Action to perform"
    )

    args = parser.parse_args()
    process_files(args.action)


if __name__ == "__main__":
    main()
