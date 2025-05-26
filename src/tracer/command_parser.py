import argparse
from tracer.config import LogDomain
from tracer.tracer_core import TracerCore

class CommandParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="tracer", description="CLI tool for tracing.")
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)

        # Subcommand: start
        self.start_parser = self.subparsers.add_parser("start", help="Start tracing")
        self.start_parser.add_argument(
            "domain", 
            choices=[d.value for d in LogDomain], 
            help="Domain to print logs for"
        )
        self.start_parser.add_argument(
            "-d", "--dir", 
            metavar="DIR", 
            required=False, 
            help="Directory to watch (required for 'file_system' domain)"
        )

        # Subcommand: logs
        self.logs_parser = self.subparsers.add_parser("show", help="Print logs")
        self.logs_parser.add_argument(
            "domain", 
            choices=[d.value for d in LogDomain], 
            help="Domain to print logs for"
        )
        self.logs_parser.add_argument(
            "-s", "--start",
            metavar="START", default=None,
            help="Start time for filtering logs "
                 "(ISO format or fuzzy: now, yesterday, or [number][s/m/h/d])."
        )
        self.logs_parser.add_argument(
            "-e", "--end",
            metavar="END", default=None,
            help="End time for filtering logs "
                 "(ISO format or fuzzy: now, yesterday, or [number][s/m/h/d])."
        )

        # Subcommand: stop
        self.stop_parser = self.subparsers.add_parser("stop", help="Stop tracing")
        self.stop_parser.add_argument(
            "domain",
            choices=[d.value for d in LogDomain],
            help="Domain to stop tracing"
        )
        self.stop_parser.add_argument(
            "-d", "--dir",
            metavar="DIR",
            required=False,
            help="Directory to stop watching (required for 'file_system' domain)"
        )

        # Subcommand: status
        self.status_parser = self.subparsers.add_parser("status", help="Show active tracers")

        # Subcommand: clear
        self.clear_parser = self.subparsers.add_parser("clear", help="Clear logs")
        self.clear_parser.add_argument(
            "domain",
            choices=[d.value for d in LogDomain],
            help="Domain to clear logs for"
        )

    def parse_args(self):
        args = self.parser.parse_args()
        tracer = TracerCore()
        
        if args.command == "start":
            tracer.start_tracing(args.domain, args.dir)
        elif args.command == "stop":
            tracer.stop_tracing(args.domain, args.dir)
        elif args.command == "status":
            tracer.show_tracing()
        elif args.command == "show":
            tracer.print_logs(args.domain, args.start, args.end)
        elif args.command == "clear":
            tracer.clear_logs(args.domain)