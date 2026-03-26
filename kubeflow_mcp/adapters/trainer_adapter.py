"""Adapter layer over kubeflow.trainer.TrainerClient."""

from collections.abc import Sequence
from dataclasses import asdict, is_dataclass
from typing import Any, TYPE_CHECKING

from kubeflow_mcp.schemas import JobSummary

if TYPE_CHECKING:
    from kubeflow.trainer import TrainerClient


class TrainerAdapter:
    """Reads trainer jobs and maps them into stable response models."""

    def __init__(self, client: "TrainerClient | None" = None):
        if client is not None:
            self._client = client
            return
        try:
            from kubeflow.trainer import TrainerClient
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "kubeflow package is required to use TrainerAdapter without an injected client."
            ) from exc
        self._client = TrainerClient()

    def list_jobs(self, runtime: str | None = None) -> Sequence[JobSummary]:
        """List jobs from SDK and map each item to JobSummary."""
        # Runtime object lookup can be added later if runtime filtering via object is needed.
        jobs = self._client.list_jobs()
        summaries = [self._to_summary(job) for job in jobs]
        if runtime:
            summaries = [job for job in summaries if job.runtime == runtime]
        return summaries

    def _to_summary(self, job: Any) -> JobSummary:
        name = getattr(job, "name", "unknown")
        status = str(getattr(job, "status", "unknown"))
        runtime = getattr(job, "runtime", None)
        created_at = getattr(job, "creation_timestamp", None) or getattr(job, "created_at", None)

        raw: dict | None = None
        if isinstance(job, dict):
            raw = job
        elif is_dataclass(job):
            raw = asdict(job)
        elif hasattr(job, "model_dump"):
            raw = job.model_dump()  # pydantic v2
        elif hasattr(job, "dict"):
            raw = job.dict()

        return JobSummary(
            name=str(name),
            status=status,
            runtime=str(runtime) if runtime is not None else None,
            created_at=str(created_at) if created_at is not None else None,
            raw=raw,
        )
