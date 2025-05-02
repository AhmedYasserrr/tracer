import argparse
from tracer.config import LogDomain


def main():
    parser = argparse.ArgumentParser(prog="tracer", description="CLI tool for tracing.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: start
    start_parser = subparsers.add_parser("start", help="Start tracing")
    start_parser.add_argument(
    "domain", 
    choices=[d.value for d in LogDomain], 
    help="Domain to print logs for"
    )
    start_parser.add_argument(
    "-d", "--dir", 
    metavar="DIR", 
    required=False, 
    help="Directory to watch (required for 'fs' domain)"
    )
    # Subcommand: logs
    logs_parser = subparsers.add_parser("logs", help="Print logs")
    logs_parser.add_argument(
        "domain", 
        choices=[d.value for d in LogDomain], 
        help="Domain to print logs for"
    )
    logs_parser.add_argument(
        "-s", "--start",
        metavar="START", default=None,
        help="Start time for filtering logs "
        "(ISO format or fuzzy: now, yesterday, or [number][s/m/h/d])."
    )
    logs_parser.add_argument(
        "-e", "--end",
        metavar="END", default=None,
        help="End time for filtering logs "
        "(ISO format or fuzzy: now, yesterday, or [number][s/m/h/d])."
    )
    args = parser.parse_args()

    if args.command == "start":
        from tracer.utils.cli_utils_tracing import start_tracing
        start_tracing(args.domain, args.dir)
    elif args.command == "logs":
        from tracer.utils.cli_utils_logRW import print_logs
        print_logs(args.domain, args.start, args.end)

if __name__ == "__main__":
    main()


