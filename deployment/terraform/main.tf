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
