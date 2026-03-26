"""MCP server bootstrap and tool registration."""

from fastmcp import FastMCP

from kubeflow_mcp.adapters.trainer_adapter import TrainerAdapter
from kubeflow_mcp.config import ServerConfig, from_env
from kubeflow_mcp.tools.jobs import get_jobs_tool


def create_server(config: ServerConfig | None = None) -> FastMCP:
    """Create and configure MCP server instance."""
    cfg = config or from_env()
    mcp = FastMCP("kubeflow-mcp")
    trainer_adapter = TrainerAdapter()

    if "trainer" in cfg.clients:
        @mcp.tool(name="get_jobs")
        def get_jobs(
            runtime: str | None = None,
            limit: int = cfg.default_limit,
            include_raw: bool = False,
        ) -> dict:
            """List training jobs from Kubeflow Trainer."""
            return get_jobs_tool(
                adapter=trainer_adapter,
                runtime=runtime,
                limit=limit,
                include_raw=include_raw,
            ).model_dump()

    return mcp
