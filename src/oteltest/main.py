import argparse

from oteltest.private import run


def main():
    parser = argparse.ArgumentParser(description="OpenTelemetry Python Tester")

    w_help = (
        "Path to an optional wheel (.whl) file to `pip install` instead of `oteltest`"
    )
    parser.add_argument("-w", "--wheel-file", type=str, required=False, help=w_help)

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
    run(args.script_dir, args.wheel_file, args.venv_parent_dir)


if __name__ == "__main__":
    main()
