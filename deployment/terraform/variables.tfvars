use_s3 = true
use_ecr = true
use_sns_sqs = true
ecr_name = "lambda_repo"
use_lambda = true
lambda_name = "main_lambda"
bucket_name = "main-video-generator"
environment_variables = {
  "LOG_LEVEL" = "DEBUG",
  "TMP_DIR" = "/tmp",
}