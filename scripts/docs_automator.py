#!/usr/bin/env python3
"""
Docs Automator - Self-Documenting Codebase Tool
Generates CHANGELOG.md, TODO.md, and STATUS.md based on code and git history.
"""

import os
import re
import subprocess
from datetime import datetime
from typing import List, Dict

# --- Configuration ---
PROJECT_ROOT = "."
EXCLUDE_DIRS = {".git", ".venv", "__pycache__", "node_modules", "htmlcov", "site"}
CHANGELOG_FILE = "CHANGELOG.md"
TODO_FILE = "TODO.md"
STATUS_FILE = "STATUS.md"

def run_command(cmd: List[str]) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

# --- Changelog Generator ---

def generate_changelog():
    print("Generating CHANGELOG.md...")
    
    # Get commits since the last tag (or all if no tags)
    last_tag = run_command(["git", "describe", "--tags", "--abbrev=0"])
    if last_tag:
        commits_range = f"{last_tag}..HEAD"
    else:
        commits_range = "HEAD"
        
    log_output = run_command(["git", "log", commits_range, "--pretty=format:%s"])
    
    if not log_output:
        print("No new commits found.")
        return

    commits = log_output.split("\n")
    
    sections = {
        "feat": [],
        "fix": [],
        "docs": [],
        "refactor": [],
        "other": []
    }
    
    for commit in commits:
        match = re.match(r"^(\w+)(\(.*\))?: (.*)", commit)
        if match:
            ctype = match.group(1)
            desc = match.group(3)
            if ctype in sections:
                sections[ctype].append(desc)
            else:
                sections["other"].append(commit)
        else:
            sections["other"].append(commit)

    # Read existing changelog
    current_content = ""
    if os.path.exists(CHANGELOG_FILE):
        with open(CHANGELOG_FILE, "r") as f:
            current_content = f.read()

    # Prepare new section
    today = datetime.now().strftime("%Y-%m-%d")
    new_section = f"## [Unreleased] - {today}\n\n"
    
    if sections["feat"]:
        new_section += "### Added\n" + "\n".join([f"- {s}" for s in sections["feat"]]) + "\n\n"
    if sections["fix"]:
        new_section += "### Fixed\n" + "\n".join([f"- {s}" for s in sections["fix"]]) + "\n\n"
    if sections["docs"]:
        new_section += "### Documentation\n" + "\n".join([f"- {s}" for s in sections["docs"]]) + "\n\n"
    if sections["refactor"]:
        new_section += "### Changed\n" + "\n".join([f"- {s}" for s in sections["refactor"]]) + "\n\n"
        
    # Check if Unreleased header already exists to avoid duplication
    if "## [Unreleased]" in current_content:
        # Simple replacement logic for demo purposes - in production might be more complex
        print("Unreleased section already exists. Skipping append.")
    else:
        final_content = new_section + current_content
        with open(CHANGELOG_FILE, "w") as f:
            f.write(final_content)

# --- Tech Debt Scanner ---

def scan_tech_debt():
    print("Scanning for TODOs...")
    todos = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Filter directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if not file.endswith((".py", ".md", ".js", ".ts", ".yml", ".yaml")):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if "TODO" in line or "FIXME" in line:
                            # Clean up line
                            clean_line = line.strip().replace("#", "").replace("//", "").strip()
                            # Remove "TODO" or "FIXME" prefix if present for cleaner output
                            clean_line = re.sub(r"^(TODO|FIXME)[:\s]*", "", clean_line)
                            
                            todos.append(f"- [ ] **{file}**:{i} - {clean_line}")
            except Exception:
                continue
                
    header = f"# Technical Debt (Auto-generated)\nLast update: {datetime.now()}\n\n"
    with open(TODO_FILE, "w") as f:
        f.write(header + "\n".join(todos))

# --- Status Dashboard ---

def generate_status():
    print("Generating STATUS.md...")
    
    # Get Python version
    python_version = run_command(["python3", "--version"])
    
    # Mock CI status retrieval (in real world, use GitHub API or local check)
    ci_status = "Unknown" 
    try:
        # Check if we can get status via ci_bridge logic purely locally? No.
        # Just placeholder for now.
        ci_status = "See GitHub Actions"
    except Exception:
        pass

    content = f"""# Project Status

**Last Update:** {datetime.now()}

## Health Indicators
| Metric | Status | Details |
|--------|--------|---------|
| **CI/CD** | ![CI](https://github.com/placeholder/repo/actions/workflows/ci.yml/badge.svg) | {ci_status} |
| **Python** | ✅ | {python_version} |
| **Documentation** | 🔄 | Auto-generated |

## Quick Links
- [Changelog](CHANGELOG.md)
- [Technical Debt](TODO.md)
- [API Docs](docs/api.md)
"""
    with open(STATUS_FILE, "w") as f:
        f.write(content)

def main():
    generate_changelog()
    scan_tech_debt()
    generate_status()
    print("Documentation updated successfully.")

if __name__ == "__main__":
    main()
