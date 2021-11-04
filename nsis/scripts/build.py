from skippy.config import RESOURCES_FOLDER, version
from skippy import __description__

from cx_Freeze import setup, Executable
import platform
import shutil
import sys
import os

path = os.path.dirname(os.path.realpath(__file__))

base = "Win32GUI" if sys.platform == "win32" else None

options = {
    "build_exe": {
        "includes": "atexit",
    }
}

executables = [
    Executable(
        os.path.join(path, "run.py"),
        icon=os.path.join(RESOURCES_FOLDER, "skippy.ico"),
        base=base,
    )
]

setup(
    name="Skippy",
    version=version,
    description=__description__,
    options=options,
    executables=executables,
)

shutil.make_archive(
    os.path.join("output", f"{platform.system()}.standalone"),
    "zip",
    os.path.join("build", "exe.win-amd64-3.9"),
)
