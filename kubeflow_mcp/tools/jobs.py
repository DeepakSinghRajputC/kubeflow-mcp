"""MCP tools for job lifecycle interactions."""

from time import perf_counter
import logging

from kubeflow_mcp.adapters.trainer_adapter import TrainerAdapter
from kubeflow_mcp.errors import KubeflowMcpError, map_exception
from kubeflow_mcp.schemas import GetJobsInput, GetJobsOutput

logger = logging.getLogger(__name__)


def get_jobs_tool(
    adapter: TrainerAdapter,
    runtime: str | None = None,
    limit: int = 50,
    include_raw: bool = False,
) -> GetJobsOutput:
    """Return normalized job list for agent use."""
    started = perf_counter()
    payload = GetJobsInput(runtime=runtime, limit=limit, include_raw=include_raw)
    try:
        jobs = list(adapter.list_jobs(runtime=payload.runtime))
        jobs.sort(key=lambda job: (job.created_at or "", job.name), reverse=True)
        total = len(jobs)
        truncated_jobs = jobs[: payload.limit]
        if not payload.include_raw:
            for job in truncated_jobs:
                job.raw = None
        result = GetJobsOutput(
            jobs=truncated_jobs,
            total=total,
            truncated=total > payload.limit,
        )
        logger.info(
            "tool=get_jobs status=ok total=%s returned=%s duration_ms=%s",
            total,
            len(result.jobs),
            int((perf_counter() - started) * 1000),
        )
        return result
    except Exception as exc:  # noqa: BLE001
        mapped: KubeflowMcpError = map_exception(exc)
        logger.warning(
            "tool=get_jobs status=error code=%s duration_ms=%s",
            mapped.code,
            int((perf_counter() - started) * 1000),
        )
        raise mapped from exc
