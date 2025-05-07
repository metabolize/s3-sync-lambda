import os
import pytest
from .testing_helpers import AWS_REGION


def test_integration(deployed_function: str) -> None:
    lambda_client = boto3.client("lambda", region_name=AWS_REGION)

    # Create a file on src
    # Ensure it's not on dst

    response = lambda_client.invoke(
        FunctionName=deployed_function,
        InvocationType="RequestResponse",
    )
    print("lambda response", response)
    print("payload", response["Payload"].read().decode("utf-8"))

    # Assert that it's on dst
