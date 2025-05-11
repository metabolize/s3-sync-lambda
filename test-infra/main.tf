terraform {
  required_providers {
    aws = {
      source  = "registry.opentofu.org/hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias = "default"
}

provider "aws" {
  alias  = "dst"
  region = "us-west-1"
}

resource "aws_s3_bucket" "src_bucket" {
  provider = aws.default
  bucket = "metabolize-s3-sync-test-src"
}

resource "aws_s3_bucket" "dst_bucket" {
  provider = aws.dst
  bucket = "metabolize-s3-sync-test-dst"
}

resource "aws_iam_role" "lambda_exec_role" {
  provider = aws.default
  name = "s3-sync-lambda-test-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

data "aws_iam_policy_document" "lambda_s3_policy" {
  statement {
    sid = "ReadFromSrcBucket"
    actions = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.src_bucket.arn}/*"]
  }

  statement {
    sid = "WriteToDstBucket"
    actions = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.dst_bucket.arn}/*"]
  }
}

resource "aws_iam_role_policy" "lambda_s3_access" {
  provider = aws.default
  name   = "lambda-s3-access-policy"
  role   = aws_iam_role.lambda_exec_role.id
  policy = data.aws_iam_policy_document.lambda_s3_policy.json
}
