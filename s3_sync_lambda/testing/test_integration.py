from botocore.exceptions import ClientError
from missouri import json
from mypy_boto3_s3.client import S3Client
from .testing_helpers import AWS_REGION, unique
from .testing_helpers import SOURCE_BUCKET, TARGET_BUCKET



def is_key_in_bucket(s3_client: S3Client, bucket: str, key: str) -> bool:
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise


def test_integration(deployed_function: str) -> None:
    import boto3

    key = f"test-{unique()}.txt"

    s3_client = boto3.client("s3")

    s3_client.put_object(
        Bucket=SOURCE_BUCKET,
        Key=key,
        Body="This is a test file.",
    )

    # Confidence check.
    assert not is_key_in_bucket(s3_client=s3_client, bucket=TARGET_BUCKET, key=key)

    response = boto3.client("lambda", region_name=AWS_REGION).invoke(
        FunctionName=deployed_function,
        InvocationType="RequestResponse",
    )
    print("lambda response", response)
    if response["FunctionError"] == "Unhandled":
        payload = json.loads(response["Payload"].read().decode("utf-8"))
        print("payload", payload)
        import pdb; pdb.set_trace()
        print(payload["errorMessage"])
        print("".join(payload["stackTrace"]))

    assert is_key_in_bucket(s3_client=s3_client, bucket=TARGET_BUCKET, key=key)
