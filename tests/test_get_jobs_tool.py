import pytest

from kubeflow_mcp.errors import KubeflowMcpError
from kubeflow_mcp.schemas import JobSummary
from kubeflow_mcp.tools.jobs import get_jobs_tool


class FakeAdapter:
    def list_jobs(self, runtime=None):
        _ = runtime
        return [
            JobSummary(
                name="job-new",
                status="Running",
                runtime="torch-distributed",
                created_at="2026-03-21T12:00:00Z",
                raw={"foo": "bar"},
            ),
            JobSummary(
                name="job-old",
                status="Complete",
                runtime="torch-distributed",
                created_at="2026-03-21T08:00:00Z",
                raw={"foo": "baz"},
            ),
        ]


class ErrorAdapter:
    def list_jobs(self, runtime=None):
        _ = runtime
        raise RuntimeError("boom")


def test_get_jobs_respects_limit_and_sort():
    result = get_jobs_tool(adapter=FakeAdapter(), limit=1)
    assert result.total == 2
    assert result.truncated is True
    assert len(result.jobs) == 1
    assert result.jobs[0].name == "job-new"
    assert result.jobs[0].raw is None


def test_get_jobs_include_raw():
    result = get_jobs_tool(adapter=FakeAdapter(), include_raw=True)
    assert result.jobs[0].raw == {"foo": "bar"}


def test_get_jobs_maps_errors():
    with pytest.raises(KubeflowMcpError) as exc_info:
        get_jobs_tool(adapter=ErrorAdapter())
    assert exc_info.value.code == "backend_error"
