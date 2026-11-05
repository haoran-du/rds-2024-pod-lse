import argparse
import json
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Paper-specific RdS reproduction; source data are read-only")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("reproduce", aliases=["validate"], help="Compute saved-basis LSE projections and scale statistics")
    validate.add_argument("--cases", nargs="+", choices=["1b", "2b", "3b", "6b", "ca"])
    commands = (validate,)
    for command in commands:
        command.add_argument("--data-root", type=Path, required=True)
        command.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    root, output = args.data_root.resolve(strict=True), args.output.resolve()
    if output == root or root in output.parents:
        parser.error("Output must be outside the read-only source data tree")
    if getattr(args, "batch", 1) < 1:
        parser.error("--batch must be positive")
    from .analysis import validate_lse
    result = validate_lse(args.data_root, args.output, args.cases)
    print(json.dumps(result, indent=2))
    if result.get("failed"):
        sys.exit(1)


if __name__ == "__main__":
    main()
