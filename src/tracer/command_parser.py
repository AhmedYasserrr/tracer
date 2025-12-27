import argparse
from tracer.config import LogDomain
from tracer.tracer_core import TracerCore


class CommandParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="tracer", description="CLI tool for tracing."
        )
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)

        # Subcommand: start
        self.start_parser = self.subparsers.add_parser("start", help="Start tracing")
        self.start_parser.add_argument(
            "domain",
            choices=[d.value for d in LogDomain],
            help="Domain to print logs for",
        )
        self.start_parser.add_argument(
            "-d",
            "--dir",
            metavar="DIR",
            required=False,
            help="Directory to watch (required for 'file_system' domain)",
        )

        # Subcommand: logs
        self.logs_parser = self.subparsers.add_parser("show", help="Print logs")
        self.logs_parser.add_argument(
            "domain",
            choices=[d.value for d in LogDomain],
            help="Domain to print logs for",
        )
        self.logs_parser.add_argument(
            "-s",
            "--start",
            metavar="START",
            default=None,
            help="Start time for filtering logs "
            "(ISO format or fuzzy: now, yesterday, or [number][s/m/h/d]).",
        )
        self.logs_parser.add_argument(
            "-e",
            "--end",
            metavar="END",
            default=None,
            help="End time for filtering logs "
            "(ISO format or fuzzy: now, yesterday, or [number][s/m/h/d]).",
        )

        # Subcommand: clear
        self.clear_parser = self.subparsers.add_parser("clear", help="Clear logs")
        self.clear_parser.add_argument(
            "domain",
            choices=[d.value for d in LogDomain],
            help="Domain to clear logs for",
        )

    def parse_args(self):
        args = self.parser.parse_args()
        tracer = TracerCore()

        if args.command == "start":
            tracer.start_tracing(args.domain, args.dir)
        elif args.command == "show":
            tracer.print_logs(args.domain, args.start, args.end)
        elif args.command == "clear":
            tracer.clear_logs(args.domain)
