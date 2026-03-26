"""Error types and mappings for MCP responses."""


class KubeflowMcpError(Exception):
    """Base MCP error with stable code."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def map_exception(exc: Exception) -> KubeflowMcpError:
    """Convert low-level exception to a user-safe MCP error."""
    if isinstance(exc, TimeoutError):
        return KubeflowMcpError(
            code="timeout",
            message="The operation timed out while contacting the Kubeflow backend.",
        )
    if isinstance(exc, ValueError):
        return KubeflowMcpError(code="invalid_request", message=str(exc))
    return KubeflowMcpError(
        code="backend_error",
        message="Failed to fetch jobs from Kubeflow backend.",
    )
