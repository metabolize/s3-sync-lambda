import sys
import typing as t
from os import environ
from os.path import dirname, join
from executor import execute


def get_aws_cli_command_line(
    source_bucket: str, source_region: str, target_bucket: str, target_region: str
) -> str:
    return " ".join(
        [
            sys.executable,
            join(dirname(__file__), "aws"),  # Path to vendored-in aws bin.
            "s3",
            "sync",
            f"s3://{source_bucket}/",
            f"s3://{target_bucket}/",
            "--source-region",
            source_region,
            "--region",
            target_region,
        ]
    )


def run_aws_s3_sync(
    source_bucket: str,
    source_region: str,
    target_bucket: str,
    target_region: str,
    verbose: bool = True,
) -> None:
    env = dict(environ)
    env["PYTHONPATH"] = ":".join(sys.path)
    execute(
        get_aws_cli_command_line(
            source_bucket=source_bucket,
            source_region=source_region,
            target_bucket=target_bucket,
            target_region=target_region,
        ),
        environment=env,
    )


def handler(event: t.Any, context: t.Any) -> None:
    run_aws_s3_sync(
        source_bucket=environ["SOURCE_BUCKET"],
        source_region=environ["SOURCE_REGION"],
        target_bucket=environ["TARGET_BUCKET"],
        target_region=environ["TARGET_REGION"],
    )


def main() -> None:
    """
    This is for local testing.
    """
    run_aws_s3_sync(
        source_bucket="metabolize-s3-sync-test-src",
        source_region="us-east-1",
        target_bucket="metabolize-s3-sync-test-dst",
        target_region="us-west-1",
    )


if __name__ == "__main__":
    main()
