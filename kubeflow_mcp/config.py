"""Runtime configuration for the MCP server."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ServerConfig:
    """Server options loaded from CLI/env."""

    clients: tuple[str, ...] = ("trainer",)
    persona: str = "readonly"
    backend: str = "kubernetes"
    namespace: str | None = None
    default_limit: int = 50


def parse_clients(raw: str | None) -> tuple[str, ...]:
    """Parse comma-separated client names."""
    if not raw:
        return ("trainer",)
    values = tuple(part.strip() for part in raw.split(",") if part.strip())
    return values or ("trainer",)


def from_env() -> ServerConfig:
    """Build config from environment variables."""
    return ServerConfig(
        clients=parse_clients(os.getenv("KUBEFLOW_MCP_CLIENTS")),
        persona=os.getenv("KUBEFLOW_MCP_PERSONA", "readonly"),
        backend=os.getenv("KUBEFLOW_MCP_BACKEND", "kubernetes"),
        namespace=os.getenv("KUBEFLOW_MCP_NAMESPACE"),
        default_limit=int(os.getenv("KUBEFLOW_MCP_DEFAULT_LIMIT", "50")),
    )
