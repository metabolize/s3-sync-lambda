#!/usr/bin/env -S poetry run python

import os
import click
from executor import execute


def python_source_files():
    import glob

    include_paths = (
        glob.glob("*.py")
        + glob.glob("s3_sync_lambda/*.py")
        + glob.glob("s3_sync_lambda/**/*.py")
    )
    exclude_paths = []
    return [x for x in include_paths if x not in exclude_paths]


@click.group()
def cli():
    pass


@cli.command()
def install():
    execute("poetry install --sync")


@cli.command()
def check_types():
    execute("mypy", "--package", "s3_sync_lambda", "--show-error-codes")


@cli.command()
def lint():
    execute("flake8", *python_source_files())


@cli.command()
def black():
    execute("black", *python_source_files())


@cli.command()
def black_check():
    execute("black", "--check", *python_source_files())


@cli.command()
def publish():
    execute("rm -rf dist/")
    execute("poetry build")
    execute("twine upload dist/*")


if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    cli()
