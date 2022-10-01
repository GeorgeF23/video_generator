output "s3_bucket_name" {
  value = var.use_s3 ? var.bucket_name : "NA"
}

output "ecr_url" {
	value = var.use_ecr ? aws_ecr_repository.ecr_repo[0].repository_url : "NA"
}

output "ecr_name" {
	value = var.use_ecr ? var.ecr_name : "NA"
}

output "sns_topic_arn" {
  value = var.use_sns_sqs ? aws_sns_topic.lambda_request_topic[0].arn : "NA"
}

output "sqs_response_url" {
  value = var.use_sns_sqs ? aws_sqs_queue.lambda_response_queue[0].id : "NA"
}