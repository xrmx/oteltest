import argparse

from oteltest.private import run


def main():
    parser = argparse.ArgumentParser(description="OpenTelemetry Python Tester")

    d_help = "An optional override directory to hold per-script venv directories."
    parser.add_argument(
        "-d", "--venv-parent-dir", type=str, required=False, help=d_help
    )

    parser.add_argument(
        "script_dir",
        type=str,
        help="The directory containing oteltest scripts at its top level",
    )

    args = parser.parse_args()
    run(args.script_dir, args.venv_parent_dir)


if __name__ == "__main__":
    main()
