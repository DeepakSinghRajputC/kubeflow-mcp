# `get_jobs` tool

## Purpose

List Kubeflow training jobs using the SDK `TrainerClient.list_jobs()` API and return a compact,
agent-safe summary payload.

## Request schema

- `runtime`: optional string runtime filter.
- `limit`: optional integer in `[1, 500]`, defaults to `50`.
- `include_raw`: optional boolean to include raw backend job payload.

## Response schema

- `jobs`: list of normalized jobs:
  - `name`
  - `status`
  - `runtime`
  - `created_at`
  - `raw` (only when `include_raw=true`)
- `total`: total jobs discovered before truncation.
- `truncated`: `true` when `total > limit`.

## Error mapping

- `timeout`: backend call exceeded timeout.
- `invalid_request`: invalid tool parameters.
- `backend_error`: unexpected SDK/backend failures.

## Notes

- This MVP intentionally starts with one tool to keep context small.
- Future expansion should keep persona and client-scoping controls enabled by default.
