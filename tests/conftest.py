import os
import sys

# Ensure repository root (parent of `tests/`) is on sys.path for `import server`
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
