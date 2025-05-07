import os
import pytest

LAMBDA_ZIP_PATH = "lambdas/s3-sync-lambda.zip"
HANDLER = "s3_sync_lambda.handler.handler"
FUNCTION_PREFIX = "s3-sync-lambda"
MEMORY_SIZE = 3008
AWS_REGION = "us-east-1"
ROLE = os.environ["LAMBDA_ROLE"]
TIMEOUT = 60
S3_CODE_BUCKET = os.environ.get("UPLOAD_BUCKET", None)


@pytest.fixture(scope="session")
def deployed_function(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> str:
    import os
    import platform
    import time
    import uuid
    import boto3
    from werkit.aws_lambda.deploy import perform_create

    client = boto3.client("lambda")
    function_name = f"{FUNCTION_PREFIX}_test_{uuid.uuid4().hex}"

    def cleanup():
        client.delete_function(FunctionName=function_name)

    assert os.path.isfile(lambda_zip_path), f"Lambda zip not found: {LAMBDA_ZIP_PATH}"

    perform_create(
        aws_region=AWS_REGION,
        local_path_to_zipfile=LAMBDA_ZIP_PATH,
        handler=HANDLER,
        function_name=function_name,
        role=ROLE,
        timeout=TIMEOUT,
        memory_size=WORKER_MEMORY_SIZE,
        s3_code_bucket=S3_CODE_BUCKET,
        verbose=True,
    )

    request.addfinalizer(cleanup)
    return function_name
