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


class App:

    """Application class
    
    Attributes:
        args (argparse.Namespace): Command-line arguments
    """
    
    def __init__(self, args: argparse.Namespace):
        """Initializing application class
        
        Args:
            args (argparse.Namespace): Command-line arguments
        """
        self.args = args

    def run(self):
        """Run application by command-line arguments
        """
        if self.args.version:
            self.version()
        elif self.args.plugins:
            self.plugins()
        else:
            self.start_ui()

    def version(self):
        """Print Skippy version
        """
        print(f"skippy v{skippy.config.version}")

    def plugins(self):
        """Print plugins list with additional data
        """
        table = PrettyTable()
        table.field_names = ["Alias", "Description", "Author", "Version"]

        for plugin in plugins.PluginLoader.plugins_data():
            table.add_row(
                [
                    plugin["__alias__"],
                    plugin["__description__"],
                    plugin["__author__"],
                    plugin["__version__"],
                ]
            )

        print(table)

    def start_ui(self):
        """Initialize everything and run the application.
        """
        logger.log.setLevel(logger.LOG_LEVELS[self.args.logging_level])

        standarddir.initdirs()
        logger.log.info("Initializing directories...")

        logger.log.info("Initializing plugin loader...")
        pluginLoader = plugins.PluginLoader()

        logger.log.info("Load plugins...")
        pluginLoader.load_plugins()

        logger.log.info("Start plugins...")
        pluginLoader.start_plugins()

        logger.log.info("Initializing Discord RPC..")
        rpc = discord_rpc.DiscordRPC()

        logger.log.info("Connect Discord RPC..")
        rpc.connect()

        logger.log.info("Initializing application...")
        exit_code = start_ui()

        logger.log.info("Stop plugins...")
        pluginLoader.stop_plugins()

        logger.log.info("Stop Discord RPC..")
        rpc.close()

        return exit_code


def run():
    """Initialize everything and run the application.
    """
    excepthook.init()

    parser = get_argparser()

    app = App(parser.parse_args())
    sys.exit(app.run())
