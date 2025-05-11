# s3-sync-lambda

Sync an S3 bucket to another S3 bucket in AWS Lambda.

This is a very light wrapper around the Python AWS CLI.


## Configuration

To use this for backup purposes, it's recommended to create the target bucket in
a different region.

The Lambda role requires permissions on the source and target S3 buckets. For
the detailed permissions, refer to the `lambda_s3_policy` in
`test-infra/main.tf`.

The Lambda should be configured with the following environment variables:

* `SOURCE_BUCKET`
* `SOURCE_REGION`
* `TARGET_BUCKET`
* `TARGET_REGION`


## Releasing

To perform a release, open a pull request with the name e.g. **RELEASE 1.0.1**,
which updates the version number in `pyproject.toml` and adds a changelog entry.
After it's merged to main, run the **Manual release** GitHub action.


## Acknowledgements

This Lambda function was initially developed by Jacob Beard.


## License

The project is licensed under the Apache License, Version 2.0.
