import argparse
from typing import Sequence
from tracer.config import LogDomain


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

        # Subcommand: stop
        self.stop_parser = self.subparsers.add_parser("stop", help="Stop tracing")
        self.stop_parser.add_argument(
            "domain",
            choices=[d.value for d in LogDomain],
            help="Domain to stop tracing for",
        )
        self.stop_parser.add_argument(
            "-d",
            "--dir",
            metavar="DIR",
            required=False,
            help="Directory to stop watching (required for 'file_system' domain)",
        )

        # Subcommand: query
        self.query_parser = self.subparsers.add_parser(
            "query", help="Execute SQL query"
        )
        self.query_parser.add_argument(
            "sql_query",
            help="SQL query to execute",
        )

        # Subcommand: list-domains
        self.list_domains_parser = self.subparsers.add_parser(
            "list-domains", help="List available tracing domains"
        )

        # Subcommand: list-tracers
        self.list_tracers_parser = self.subparsers.add_parser(
            "list-tracers", help="List active tracers"
        )

        # Subcommand: clear
        self.clear_parser = self.subparsers.add_parser("clear", help="Clear logs")
        self.clear_parser.add_argument(
            "domain",
            choices=[d.value for d in LogDomain],
            help="Domain to clear logs for",
        )

        # Subcommand: reset
        self.reset_parser = self.subparsers.add_parser("reset", help="Reset database")

        # Subcommand: schema
        self.schema_parser = self.subparsers.add_parser(
            "schema", help="Read database table schema"
        )
        self.schema_parser.add_argument(
            "domain",
            choices=[d.value for d in LogDomain],
            help="Domain to read schema for",
        )

    def parse_args(self, argv: Sequence[str] | None) -> argparse.Namespace:
        return self.parser.parse_args(argv)
