import argparse
from tracer.store.log_reader import LogReader
from tracer.store.log_writer import LogWriter
from tracer.config import LogDomain
from tracer.core.base_tracer import BaseTracer
from tracer.core.fs_tracer import FileTracer

def start_tracing(domain: str, dir_to_watch: str = None):
    """Starts tracing for the specified domain."""
    if domain == "fs":
        if not dir_to_watch:
            print("Error: --dir is required for the 'fs' domain.")
            return
        print("Starting filesystem tracing...")
        # Replace with actual FileTracer implementation
        tracer = FileTracer(LogWriter(LogDomain.FS), dir_to_watch)
        tracer.start()
    elif domain == "net":
        print("Starting network tracing...")
        # Replace with actual NetTracer implementation
        tracer = BaseTracer(LogWriter(LogDomain.NET))
        tracer.start()
    else:
        print(f"Unknown domain: {domain}")

def print_logs(domain: str, start_time: str = None, end_time: str = None):
    """Prints logs for the specified domain and time range."""
    log_domain = next((d for d in LogDomain if d.value == domain), None)
    if log_domain is None:
        print(f"Unknown domain: {domain}")
        return

    reader = LogReader(log_domain)
    reader.print_logs(start_time, end_time)

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
        start_tracing(args.domain, args.dir)
    elif args.command == "logs":
        print_logs(args.domain, args.start, args.end)

if __name__ == "__main__":
    main()


