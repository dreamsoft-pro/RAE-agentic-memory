#!/usr/bin/env python3
"""
Docs Automator - Self-Documenting Codebase Tool
Generates/Updates CHANGELOG.md, TODO.md, STATUS.md, and TESTING_STATUS.md.
"""

import os
import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Optional

# --- Configuration ---
PROJECT_ROOT = "."
EXCLUDE_DIRS = {".git", ".venv", "__pycache__", "node_modules", "htmlcov", "site", "alembic"}
CHANGELOG_FILE = "CHANGELOG.md"
TODO_FILE = "TODO.md"
STATUS_FILE = "STATUS.md"
TESTING_FILE = "docs/TESTING_STATUS.md"
COVERAGE_FILE = "coverage.xml"
JUNIT_FILE = "junit.xml"

def run_command(cmd: List[str]) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

# --- Helpers ---

def get_file_content(path: str) -> str:
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def write_file_content(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)

# --- Data Providers ---

def get_coverage_stats() -> Optional[float]:
    """Parses coverage.xml to get line coverage percentage."""
    if not os.path.exists(COVERAGE_FILE):
        return None
    try:
        tree = ET.parse(COVERAGE_FILE)
        root = tree.getroot()
        return float(root.attrib.get("line-rate", 0)) * 100
    except Exception:
        return None

def get_test_stats() -> Dict[str, int]:
    """Parses junit.xml to get test results."""
    stats = {"total": 0, "failures": 0, "errors": 0, "skipped": 0}
    if not os.path.exists(JUNIT_FILE):
        return stats
    try:
        tree = ET.parse(JUNIT_FILE)
        root = tree.getroot()
        # JUnit XML structure varies, usually root is testsuites or testsuite
        if root.tag == "testsuites":
            for suite in root:
                stats["total"] += int(suite.attrib.get("tests", 0))
                stats["failures"] += int(suite.attrib.get("failures", 0))
                stats["errors"] += int(suite.attrib.get("errors", 0))
                stats["skipped"] += int(suite.attrib.get("skipped", 0))
        elif root.tag == "testsuite":
            stats["total"] += int(root.attrib.get("tests", 0))
            stats["failures"] += int(root.attrib.get("failures", 0))
            stats["errors"] += int(root.attrib.get("errors", 0))
            stats["skipped"] += int(root.attrib.get("skipped", 0))
    except Exception:
        pass
    return stats

def get_git_branch() -> str:
    return run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or "unknown"

def get_git_hash() -> str:
    return run_command(["git", "rev-parse", "--short", "HEAD"]) or "unknown"

# --- Generators ---

def update_todo():
    print(f"Updating {TODO_FILE}...")
    current_content = get_file_content(TODO_FILE)
    
    # Scan for TODOs in code
    todos = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if not file.endswith((".py", ".md", ".js", ".ts", ".yml", ".yaml", ".sh")):
                continue
            file_path = os.path.join(root, file)
            if file_path == os.path.join(PROJECT_ROOT, TODO_FILE): continue
            
            try:
                with open(file_path, "r", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if "TODO" in line or "FIXME" in line:
                            clean_line = line.strip().replace("#", "").replace("//", "").strip()
                            clean_line = re.sub(r"^(TODO|FIXME)[:\s]*", "", clean_line)
                            # Format: - [ ] **file:line** - text
                            rel_path = os.path.relpath(file_path, PROJECT_ROOT)
                            todos.append(f"- [ ] **{rel_path}:{i}** - {clean_line}")
            except Exception:
                continue

    tech_debt_section = "## Technical Debt (Auto-generated from code)\n" + \
                        (f"*Last scan: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n" if todos else "\n") + \
                        "\n".join(todos) if todos else "No TODOs found in code."

    # Inject into TODO.md
    marker = "## Technical Debt (Auto-generated from code)"
    
    if marker in current_content:
        # Replace everything after the marker
        parts = current_content.split(marker)
        new_content = parts[0] + tech_debt_section
    else:
        # Append to end
        new_content = current_content + "\n\n" + tech_debt_section
        
    write_file_content(TODO_FILE, new_content)

def update_status():
    print(f"Updating {STATUS_FILE}...")
    content = get_file_content(STATUS_FILE)
    
    # Metrics
    cov = get_coverage_stats()
    tests = get_test_stats()
    branch = get_git_branch()
    commit = get_git_hash()
    
    # Basic replacement logic (regex would be better but let's keep it simple for now)
    # We will look for specific rows to update or append a "Live Metrics" section
    
    cov_str = f"{cov:.1f}%" if cov is not None else "N/A"
    test_pass_rate = 0
    if tests["total"] > 0:
        test_pass_rate = ((tests["total"] - tests["failures"] - tests["errors"]) / tests["total"]) * 100
    
    metrics_md = f"""
## Live Metrics (Auto-generated)
| Metric | Value |
|--------|-------|
| **Branch** | `{branch}` |
| **Commit** | `{commit}` |
| **Coverage** | {cov_str} |
| **Tests** | {tests['total']} total, {tests['failures']} failed, {tests['skipped']} skipped |
| **Pass Rate** | {test_pass_rate:.1f}% |
| **Last Update** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
"""
    
    marker = "## Live Metrics (Auto-generated)"
    if marker in content:
        parts = content.split(marker)
        # Try to find the next section start (##) to preserve footer if any
        rest = parts[1]
        next_section_match = re.search(r"\n## ", rest)
        if next_section_match:
            footer = rest[next_section_match.start():]
            new_content = parts[0] + metrics_md + footer
        else:
            new_content = parts[0] + metrics_md
    else:
        # Insert before "Quick Links" if exists, else append
        if "## Quick Links" in content:
            new_content = content.replace("## Quick Links", metrics_md + "\n## Quick Links")
        else:
            new_content = content + "\n" + metrics_md
            
    write_file_content(STATUS_FILE, new_content)

def update_testing_status():
    print(f"Updating {TESTING_FILE}...")
    tests = get_test_stats()
    cov = get_coverage_stats()
    
    if not tests["total"] and not cov:
        print("No test data found. Skipping TESTING_STATUS update.")
        return

    content = f"""# Testing Status

**Last Run:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Commit:** {get_git_hash()}

## Summary
- **Total Tests:** {tests['total']}
- **Passed:** {tests['total'] - tests['failures'] - tests['errors']}
- **Failed:** {tests['failures']}
- **Errors:** {tests['errors']}
- **Skipped:** {tests['skipped']}
- **Coverage:** {f"{cov:.2f}%" if cov else "N/A"}

## Coverage Report
See `htmlcov/index.html` for detailed report.

## Test Suite Health
{'🟢 Excellent' if tests['failures'] == 0 and (cov or 0) > 80 else '🟡 Good' if tests['failures'] == 0 else '🔴 Failing'}
"""
    # Check if dir exists
    os.makedirs(os.path.dirname(TESTING_FILE), exist_ok=True)
    write_file_content(TESTING_FILE, content)

def main():
    print("🤖 Docs Automator - Starting...")
    try:
        update_todo()
        update_status()
        update_testing_status()
        # We skip changelog for now to avoid git noise, it should be handled by release workflow
        print("✅ Documentation updated successfully.")
    except Exception as e:
        print(f"❌ Error updating documentation: {e}")
        exit(1)

if __name__ == "__main__":
    main()