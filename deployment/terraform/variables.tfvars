use_s3 = true
use_ecr = true
ecr_name = "lambda_repo"
use_lambda = true
lambda_name = "main_lambda"

environment_variables = {
  "LOG_LEVEL" = "DEBUG",
  "TMP_DIR" = "/tmp"
}