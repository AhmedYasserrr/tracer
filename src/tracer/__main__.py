import sys
import asyncio
from collections.abc import Sequence
from tracer.cli import (
    CommandParser,
    MCPClient,
    CommandInterface,
)


async def run_app(argv: Sequence[str] | None = None) -> None:
    args = CommandParser().parse_args(argv)

    async with MCPClient("http://127.0.0.1:9999/mcp") as client:
        if args.command == "start":
            result = await CommandInterface.start_tracing(client, args.domain, args.dir)
            print(result)
        elif args.command == "stop":
            result = await CommandInterface.stop_tracing(client, args.domain, args.dir)
            print(result)
        elif args.command == "show":
            result = await CommandInterface.show_logs(client, args.domain)
            print(result)
        elif args.command == "clear":
            result = await CommandInterface.clear_logs(client, args.domain)
            print(result)
        elif args.command == "query":
            result = await CommandInterface.execute_sql_query(client, args.sql_query)
            print(result)
        elif args.command == "list-domains":
            result = await CommandInterface.list_domains(client)
            print(result)
        elif args.command == "list-tracers":
            result = await CommandInterface.list_tracers(client)
            print(result)
        elif args.command == "reset":
            result = await CommandInterface.reset_database(client)
            print(result)
        elif args.command == "schema":
            await CommandInterface.read_db_table(client, args.domain)


def main():
    """Sync entry point for the console script."""
    try:
        # This is what executes the coroutine and waits for it
        asyncio.run(run_app())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
