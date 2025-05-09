import os
import pytest

LAMBDA_ZIP_PATH = "lambdas/s3-sync-lambda.zip"
HANDLER = "s3_sync_lambda.handler.handler"
FUNCTION_PREFIX = "s3-sync-lambda"
MEMORY_SIZE = 3008
AWS_REGION = "us-east-1"
ROLE = os.environ["LAMBDA_ROLE"]
TIMEOUT = 60
# S3_CODE_BUCKET = os.environ.get("UPLOAD_BUCKET", None)


def unique() -> str:
    import uuid

    return uuid.uuid4().hex


@pytest.fixture(scope="session")
def deployed_function(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> str:
    import os
    import boto3
    from werkit.aws_lambda.deploy import perform_create

    client = boto3.client("lambda")
    function_name = f"{FUNCTION_PREFIX}_test_{unique()}"

    def cleanup() -> None:
        client.delete_function(FunctionName=function_name)

    assert os.path.isfile(LAMBDA_ZIP_PATH), f"Lambda zip not found: {LAMBDA_ZIP_PATH}"

    perform_create(
        aws_region=AWS_REGION,
        local_path_to_zipfile=LAMBDA_ZIP_PATH,
        handler=HANDLER,
        function_name=function_name,
        role=ROLE,
        timeout=TIMEOUT,
        memory_size=MEMORY_SIZE,
        # s3_code_bucket=S3_CODE_BUCKET,
        verbose=True,
    )

    request.addfinalizer(cleanup)
    return function_name
