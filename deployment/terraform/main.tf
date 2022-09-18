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
  bucket = "main-video-generator"
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

output "s3_bucket_name" {
  value = var.use_s3 ? aws_s3_bucket.main_bucket[0].bucket_domain_name : "NA"
}

output "ecr_url" {
	value = var.use_ecr ? aws_ecr_repository.ecr_repo[0].repository_url : "NA"
}

output "ecr_name" {
	value = var.use_ecr ? var.ecr_name : "NA"
}
