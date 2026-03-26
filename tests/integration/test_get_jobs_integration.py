import pytest

from kubeflow_mcp.schemas import JobSummary
from kubeflow_mcp.tools.jobs import get_jobs_tool


@pytest.mark.integration
def test_get_jobs_contract_shape():
    class IntegrationAdapter:
        def list_jobs(self, runtime=None):
            _ = runtime
            return [
                JobSummary(
                    name="job-1",
                    status="Complete",
                    runtime="torch-distributed",
                    created_at="2026-03-21T00:00:00Z",
                )
            ]

    output = get_jobs_tool(adapter=IntegrationAdapter())
    assert output.model_dump().keys() == {"jobs", "total", "truncated"}
