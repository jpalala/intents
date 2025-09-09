#!/usr/bin/env python3
import re
import json
import argparse
import subprocess
from pathlib import Path
import shutil

# Supported comment prefixes
COMMENT_PREFIXES = ["#", "//", "--"]
# File extensions for Python fallback scan
SEARCH_EXTENSIONS = [".py", ".php", ".js", ".ts", ".cpp", ".c", ".sh", ".java", ".sql"]

# Compile regex for Python scanning
pattern = re.compile(
    r'(?:' + '|'.join(re.escape(p) for p in COMMENT_PREFIXES) + r')\s*@intent:\s*(.+)',
    re.IGNORECASE
)

def find_intents_ag(root_dir="."):
    """
    Attempt to use 'ag' (The Silver Searcher) for fast scanning.

    Explanation:
    - 'ag' is a C-based tool optimized for recursive text search.
    - If 'ag' is installed, it will scan the given root directory for
      '@intent:' comments much faster than Python can.
    - The function parses 'ag' output and converts it into a list of dictionaries
      containing 'file', 'line', and 'intent'.
    - If 'ag' is not available, this function returns None and the caller
      should fallback to Python-based scanning.
    """
    if shutil.which("ag") is None:
        return None

    results = []
    cmd = ["ag", "-H", "-n", r"@intent:", root_dir]
    try:
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        for line in process.stdout.splitlines():
            try:
                file_path, line_no, content = line.split(":", 2)
                results.append({
                    "file": file_path,
                    "line": int(line_no),
                    "intent": content.strip()
                })
            except ValueError:
                continue
    except subprocess.CalledProcessError:
        return None
    return results

def find_intents_python(root_dir="."):
    """Fallback: pure Python scanning for @intent comments."""
    results = []
    for path in Path(root_dir).rglob("*.*"):
        if path.suffix.lower() in SEARCH_EXTENSIONS:
            try:
                with path.open(encoding="utf-8", errors="ignore") as f:
                    for line_no, line in enumerate(f, start=1):
                        match = pattern.search(line)
                        if match:
                            results.append({
                                "file": str(path),
                                "line": line_no,
                                "intent": match.group(1).strip()
                            })
            except Exception as e:
                print(f"Warning: Could not read {path}: {e}")
    return results

# @intent: entry-point
def main():
    parser = argparse.ArgumentParser(description="Parse code files for @intent comments")
    parser.add_argument("root", nargs="?", default=".", help="Root directory to search (default: current dir)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    results = find_intents_ag(args.root)
    if results is None:
        print("Notice: 'ag' not found. Falling back to Python scan (slower).")
        results = find_intents_python(args.root)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"{r['file']}:{r['line']} - {r['intent']}")

if __name__ == "__main__":
    main()
