from typing import Any
import setuptools
import ast
import re
import os

try:
    BASEDIR = os.path.dirname(os.path.realpath(__file__))
except NameError:
    BASEDIR = None


def read_file(name: str) -> str:
    """Get the string contained in the file named name.

    Args:
        name (str): File name

    Returns:
        str: File content
    """
    with open(name, "r", encoding="utf8") as f:
        return f.read()


def _get_constant(name: str) -> Any:
    """Read a __magic__ constant from skippy/__init__.py.

    We don't import Skippy here because it can go wrong for multiple
    reasons. Instead we use re/ast to get the value directly from the source
    file.

    Args:
        name: The name of the argument to get.

    Return:
        The value of the argument.
    """
    field_re = re.compile(r"__{}__\s+=\s+(.*)".format(re.escape(name)))
    path = os.path.join(BASEDIR, "skippy", "__init__.py")
    line = field_re.search(read_file(path)).group(1)
    value = ast.literal_eval(line)
    return value


readme = read_file("README.md")
requirements = read_file("requirements.txt").splitlines()

setuptools.setup(
    name="skippy-pad",
    version=_get_constant("version"),
    description=_get_constant("description"),
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/skippy-dev/skippy/",
    author=_get_constant("author"),
    author_email=_get_constant("email"),
    python_requires=">=3.7",
    license=_get_constant("license"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=["scp", "wikidot", "pyscp", "skippy"],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    extras_require={
        "ftml": ["pyftml==0.1.2"],
    },
    package_dir={"skippy": "skippy"},
    package_data={
        "skippy": [
            "resources/*",
            "resources/*/*",
            "lang/*.toml"
        ]
    },
    entry_points={
        "console_scripts": [
            "skippy = skippy.app:run",
        ],
    },
)
