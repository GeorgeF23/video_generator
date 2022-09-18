variable "use_s3" {
	description = "whether or not to use s3"
}

variable "use_ecr" {
	description = "whether or not to use ecr"
}

variable "ecr_name" {
  description = "the name of the ecr repository"
}

variable "use_lambda" {
  description = "whether or not to use lambda"
}

variable "lambda_name" {
  description = "lambda name"
}

variable "environment_variables" {
  type = map(string)
  description = "environment variables to pass to lambda"
  default = {
  }

}