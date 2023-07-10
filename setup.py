"""A setuptools based setup module."""

import pathlib

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

import docraise

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="docraise",  # Required
    version=docraise.__version__,  # Required
    description='Docraise is a linter that checks whether the docstrings contain valid "Raises" sections',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional
    url="https://github.com/Laleee/docraise",  # Optional
    author="Lazar Jovanovic",  # Optional
    author_email="jlazar1996@gmail.com",  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="lint",  # Optional
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),  # Required
    python_requires=">=3.8",
    install_requires=["docstring_parser", "click"],
    entry_points={
        "console_scripts": [
            "docraise=docraise.main:main",
        ],
    },
    project_urls={  # Optional
        "Source": "https://github.com/Laleee/docraise",
    },
)
