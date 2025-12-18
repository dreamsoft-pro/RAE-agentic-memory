from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Determine the absolute path to the project root.
# Assumption: this file is located in <PROJECT_ROOT>/core/paths.py
# So we resolve this file, go up 2 levels (core -> root).
DEFAULT_ROOT = Path(__file__).resolve().parents[1]

# Allow override via environment variable (crucial for Docker/CI)
PROJECT_ROOT = Path(
    os.getenv("RAE_PROJECT_ROOT", DEFAULT_ROOT)
).resolve()

# --- Standard Directories ---

# Data directory (persistent storage)
DATA_DIR = PROJECT_ROOT / "data"

# Memory storage (files, vectors, databases setup)
MEMORY_DIR = DATA_DIR / "memory"

# Cache directory (temporary artifacts)
CACHE_DIR = DATA_DIR / "cache"

# Logs directory
LOGS_DIR = DATA_DIR / "logs"

# Configuration directory
CONFIG_DIR = PROJECT_ROOT / "config"

# Temporary directory (safe to clean)
TEMP_DIR = DATA_DIR / "tmp"

# Benchmarking results
BENCHMARKS_DIR = PROJECT_ROOT / "benchmarking"
BENCHMARK_RESULTS_DIR = BENCHMARKS_DIR / "results"

# Ensure critical directories exist
for directory in [DATA_DIR, MEMORY_DIR, CACHE_DIR, LOGS_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Helper function to print setup (for debugging)
def print_debug_paths():
    print(f"RAE Paths Configuration:")
    print(f"  PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"  DATA_DIR:     {DATA_DIR}")
    print(f"  CONFIG_DIR:   {CONFIG_DIR}")
    print(f"  LOGS_DIR:     {LOGS_DIR}")
