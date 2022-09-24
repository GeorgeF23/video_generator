terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_s3_bucket" "main_bucket" {
  count = var.use_s3 ? 1 : 0
  bucket = var.bucket_name
}

resource "aws_s3_bucket_acl" "main_bucket_acl" {
  count = var.use_s3 ? 1 : 0
  bucket = aws_s3_bucket.main_bucket[0].id
  acl = "private"
}

resource "aws_ecr_repository" "ecr_repo" {
  count = var.use_ecr ? 1 : 0
  name = var.ecr_name
}

resource "aws_iam_role" "iam_for_lambda" {
  count = var.use_lambda ? 1 : 0
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "lambda_logging" {
  count = var.use_lambda ? 1 : 0
  name        = "${var.lambda_name}-logging"
  path        = "/"
  description = "IAM policy for logging from the lambda function"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    },
    {
      "Action": "cloudwatch:PutMetricData",
      "Resource": "*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "lambda_s3" {
	count = var.use_s3 && var.use_lambda ? 1 : 0
	name = "${var.lambda_name}-s3-policy"
	description = "S3 policy for lambda"
	policy = <<EOF
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"s3:*"
			],
			"Resource": "arn:aws:s3:::*"
		}
	]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_s3" {
	count = var.use_s3 && var.use_lambda ? 1 : 0
	role = aws_iam_role.iam_for_lambda[0].name
	policy_arn = aws_iam_policy.lambda_s3[0].arn
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  count = var.use_lambda ? 1 : 0
  role       = aws_iam_role.iam_for_lambda[0].name
  policy_arn = aws_iam_policy.lambda_logging[0].arn
}

resource "aws_cloudwatch_log_group" "cw_log_group" {
  count = var.use_lambda ? 1 : 0
  name              = "/aws/lambda/${var.lambda_name}"
  retention_in_days = 14
}


resource "aws_lambda_function" "main_lambda" {
  count = var.use_lambda && var.use_ecr ? 1 : 0
  function_name = var.lambda_name
  role = aws_iam_role.iam_for_lambda[0].arn
  memory_size = 3000
  image_config {
    command = ["main.handler"]
  }
  package_type = "Image"
  image_uri = "${aws_ecr_repository.ecr_repo[0].repository_url}:latest"
  timeout = 600

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs[0],
    aws_cloudwatch_log_group.cw_log_group[0],
	aws_iam_role_policy_attachment.lambda_s3[0]
  ]

  environment {
    variables = merge(var.environment_variables, {
		"S3_BUCKET" = var.bucket_name
	})
  }
}

output "s3_bucket_name" {
  value = var.use_s3 ? var.bucket_name : "NA"
}

output "ecr_url" {
	value = var.use_ecr ? aws_ecr_repository.ecr_repo[0].repository_url : "NA"
}

output "ecr_name" {
	value = var.use_ecr ? var.ecr_name : "NA"
}
