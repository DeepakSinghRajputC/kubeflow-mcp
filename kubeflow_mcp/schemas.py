"""Pydantic request/response schemas for MCP tools."""

from pydantic import BaseModel, Field


class GetJobsInput(BaseModel):
    """Tool input for listing jobs."""

    runtime: str | None = Field(default=None, description="Optional runtime name filter")
    limit: int = Field(default=50, ge=1, le=500, description="Maximum jobs to return")
    include_raw: bool = Field(
        default=False,
        description="When true, include raw backend representation (best effort)",
    )


class JobSummary(BaseModel):
    """Agent-friendly summary of a training job."""

    name: str
    status: str
    runtime: str | None = None
    created_at: str | None = None
    raw: dict | None = None


class GetJobsOutput(BaseModel):
    """Tool output for listed jobs."""

    jobs: list[JobSummary]
    total: int
    truncated: bool = False
