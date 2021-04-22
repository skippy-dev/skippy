from prettytable import PrettyTable
import argparse
import sys

import skippy.app
import skippy.config

from skippy.utils.logger import log
import skippy.utils.plugin


def get_argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="print the version - will not run the ui",
    )
    parser.add_argument(
        "-p",
        "--plugins",
        action="store_true",
        help="print plugin list - will not run the ui",
    )
    parser.add_argument(
        "--logging_level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="the level to use for logging - defaults to INFO",
        default="INFO",
    )

    return parser


def run():
    parser = get_argparser()

    args = parser.parse_args()
    log.setLevel(skippy.utils.logger.LOG_LEVELS[args.logging_level])

    if args.version:
        log.info(f"skippy v{skippy.config.version}")
    elif args.plugins:
        table = PrettyTable()
        table.field_names = ["Alias", "Description", "Author", "Version"]
        sys.path.append(skippy.config.PLUGINS_FOLDER)
        for plugin in skippy.utils.plugin.PluginLoader.plugins_data():
            table.add_row(
                [
                    plugin["__alias__"],
                    plugin["__description__"],
                    plugin["__author__"],
                    plugin["__version__"],
                ]
            )
        print(table)
    else:
        log.debug("Initializing application...")
        skippy.utils.plugin.PluginLoader()
        skippy.app.start_ui()


if __name__ == "__main__":
    run()
