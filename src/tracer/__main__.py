from collections.abc import Sequence
from tracer.tracer_core import TracerCore
from .command_parser import CommandParser


def main(argv: Sequence[str] | None = None) -> None:
    args = CommandParser().parse_args(argv)
    tracer = TracerCore()
    if args.command == "start":
        tracer.start_tracing(args.domain, args.dir)
    elif args.command == "show":
        tracer.print_logs(args.domain, args.start, args.end)
    elif args.command == "clear":
        tracer.clear_logs(args.domain)


if __name__ == "__main__":
    raise SystemExit(main(None))
