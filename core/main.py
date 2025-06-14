import argparse


def main(argv=None):
    """Unified command-line entry point for AutoNest."""
    parser = argparse.ArgumentParser(description="AutoNest launcher")
    parser.add_argument(
        "mode",
        choices=["gui", "cli", "restore"],
        nargs="?",
        default="gui",
        help="Start GUI (default), CLI or restore tool",
    )
    args = parser.parse_args(argv)

    if args.mode == "gui":
        from interface.autonest_gui import main as gui_main

        gui_main()
    elif args.mode == "cli":
        from interface.autonest_cli import main as cli_main

        cli_main()
    else:  # restore
        from interface.restore_tool import main as restore_main

        restore_main()


if __name__ == "__main__":
    main()
