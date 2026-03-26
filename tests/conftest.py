"""Test configuration.

This repo's root contains multiple projects; when running `pytest` from the monorepo root,
Python may not include `kubeflow-mcp/` on `sys.path`. Add it here so imports like
`from kubeflow_mcp...` work consistently.
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def pytest_configure(config) -> None:  # pragma: no cover
    # Register markers even when pytest is invoked from a monorepo root where
    # kubeflow-mcp/pyproject.toml isn't picked up as the configfile.
    config.addinivalue_line(
        "markers",
        "integration: marks tests that validate integration behavior",
    )

