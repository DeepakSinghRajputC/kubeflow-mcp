# kubeflow-mcp

Minimal MCP server for Kubeflow SDK with an initial `get_jobs` tool.

## What this MVP includes

- MCP server bootstrap and CLI (`kubeflow-mcp serve`)
- `get_jobs` tool backed by `kubeflow.trainer.TrainerClient.list_jobs()`
- Stable response schema for agent consumption
- Unit and integration tests for tool behavior
- Initial guardrails for errors, truncation, and logging

## Install

```bash
pip install -e ".[dev]"
```

## Run server

```bash
kubeflow-mcp serve --clients trainer --persona readonly --default-limit 50
```

## Tool: `get_jobs`

Input:

- `runtime` (optional string)
- `limit` (optional int, default 50)
- `include_raw` (optional bool, default false)

Output:

- `jobs` (array)
- `total` (int)
- `truncated` (bool)

## Example MCP client config

```json
{
  "mcpServers": {
    "kubeflow": {
      "command": "kubeflow-mcp",
      "args": ["serve", "--clients", "trainer", "--persona", "readonly"]
    }
  }
}
```

## Development checks

```bash
pytest
ruff check .
```

## Risks and guardrails (MVP)

- Multi-tenant namespace leakage is possible without explicit auth context.
- Large job lists can overflow context; `limit` + `truncated` reduce payload size.
- Backend exceptions are mapped to stable, user-safe MCP errors.
