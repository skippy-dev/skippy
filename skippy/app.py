"""Initialization of Skippy and application-wide things.
"""
from skippy.gui import start_ui

from skippy.core import plugins

from skippy.utils import logger, standarddir, discord_rpc, excepthook
import skippy.config

from prettytable import PrettyTable
import argparse
import sys


def get_argparser() -> argparse.ArgumentParser:
    """Get the argument parser.

    Returns:
        argparse.ArgumentParser: Argument parser
    """
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
    """Initialize everything and run the application.
    """
    excepthook.init()

    parser = get_argparser()

    args = parser.parse_args()

    logger.log.setLevel(logger.LOG_LEVELS[args.logging_level])

    standarddir.initdirs()

    if args.version:
        logger.log.info(f"skippy v{skippy.config.version}")
    elif args.plugins:
        table = PrettyTable()
        table.field_names = ["Alias", "Description", "Author", "Version"]

        for plugin in plugins.PluginLoader.pluginsData():
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
        logger.log.info("Initializing directories...")

        logger.log.info("Initializing plugin loader...")
        pluginLoader = plugins.PluginLoader()

        logger.log.info("Load plugins...")
        pluginLoader.loadPlugins()

        logger.log.info("Start plugins...")
        pluginLoader.startPlugins()

        logger.log.info("Initializing Discord RPC..")
        rpc = discord_rpc.DiscordRPC()

        logger.log.info("Connect Discord RPC..")
        rpc.connect()

        logger.log.info("Initializing application...")
        exit_code = start_ui()

        logger.log.info("Stop plugins...")
        pluginLoader.stopPlugins()

        logger.log.info("Stop Discord RPC..")
        rpc.close()

        sys.exit(exit_code)
