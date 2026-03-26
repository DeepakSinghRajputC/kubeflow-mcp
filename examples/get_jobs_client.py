"""Minimal example invoking local MCP tool logic for get_jobs."""

from kubeflow_mcp.adapters.trainer_adapter import TrainerAdapter
from kubeflow_mcp.tools.jobs import get_jobs_tool


def main() -> None:
    adapter = TrainerAdapter()
    result = get_jobs_tool(adapter=adapter, limit=10, include_raw=False)
    print(result.model_dump())


if __name__ == "__main__":
    main()
