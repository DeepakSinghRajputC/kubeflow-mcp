from dataclasses import dataclass

from kubeflow_mcp.adapters.trainer_adapter import TrainerAdapter


@dataclass
class FakeJob:
    name: str
    status: str
    runtime: str
    created_at: str


class FakeClient:
    def list_jobs(self):
        return [
            FakeJob(
                name="job-a",
                status="Running",
                runtime="torch-distributed",
                created_at="2026-03-21T10:00:00Z",
            ),
            FakeJob(
                name="job-b",
                status="Complete",
                runtime="xgboost",
                created_at="2026-03-21T09:00:00Z",
            ),
        ]


def test_list_jobs_maps_to_summary():
    adapter = TrainerAdapter(client=FakeClient())
    jobs = adapter.list_jobs()
    assert len(jobs) == 2
    assert jobs[0].name == "job-a"
    assert jobs[0].status == "Running"
    assert jobs[0].runtime == "torch-distributed"


def test_list_jobs_runtime_filter():
    adapter = TrainerAdapter(client=FakeClient())
    jobs = adapter.list_jobs(runtime="xgboost")
    assert len(jobs) == 1
    assert jobs[0].name == "job-b"
