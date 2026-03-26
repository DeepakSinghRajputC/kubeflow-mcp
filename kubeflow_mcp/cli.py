"""CLI entrypoint for kubeflow-mcp."""

import argparse

from kubeflow_mcp.config import ServerConfig, parse_clients
from kubeflow_mcp.server import create_server


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kubeflow-mcp")
    subparsers = parser.add_subparsers(dest="command", required=True)
    serve = subparsers.add_parser("serve", help="Run MCP server")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--clients", default="trainer")
    serve.add_argument("--persona", default="readonly")
    serve.add_argument("--backend", default="kubernetes")
    serve.add_argument("--namespace", default=None)
    serve.add_argument("--default-limit", type=int, default=50)
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    if args.command == "serve":
        config = ServerConfig(
            clients=parse_clients(args.clients),
            persona=args.persona,
            backend=args.backend,
            namespace=args.namespace,
            default_limit=args.default_limit,
        )
        app = create_server(config)
        app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
