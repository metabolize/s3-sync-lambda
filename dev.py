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


def build_lambda_with_poetry_dependencies(
    target_path: str,
    build_dir: str = "build",
    src_files: list[str] = [],
    src_dirs: list[str] = [],
    lib_files: list[str] = [],
    verbose: bool = False,
) -> None:
    import os
    import shutil
    from werkit.aws_lambda.build import (
        collect_zipfile_contents,
        create_venv_with_dependencies,
        create_zipfile_from_dir,
        export_poetry_requirements,
    )

    shutil.rmtree(build_dir, ignore_errors=True)
    os.makedirs(build_dir, exist_ok=True)

    exported_requirements_file = os.path.join(build_dir, "requirements.txt")
    export_poetry_requirements(output_file=exported_requirements_file)

    venv_dir = os.path.join(build_dir, "venv")
    create_venv_with_dependencies(
        venv_dir=venv_dir,
        upgrade_pip=True,
        install_wheel=True,
        install_requirements_from=[exported_requirements_file],
        install_transitive_dependencies=False,
    )

    contents_dir = os.path.join(build_dir, "contents")
    collect_zipfile_contents(
        target_dir=contents_dir,
        venv_dir=venv_dir,
        src_dirs=src_dirs,
        src_files=src_files,
        verbose=verbose,
    )

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    create_zipfile_from_dir(dir_path=contents_dir, path_to_zipfile=target_path)


def perform_build() -> None:
    build_lambda_with_poetry_dependencies(
        src_dirs=["s3_sync_lambda"],
        target_path="lambdas/s3-sync-lambda.zip",
    )


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
def test():
    execute("pytest")


@cli.command()
def build():
    perform_build()


@cli.command()
def publish():
    execute("rm -rf dist/")
    execute("poetry build")
    execute("twine upload dist/*")


if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    cli()
