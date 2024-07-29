variable "region" {
  description = "The AWS region to use for the backend"
  type        = string
  default     = "us-east-2"
}

variable "bucket_name" {
  description = "The name of the S3 bucket to use for the backend"
  type        = string
  default     = "terraform-state-mlops-bootcamp"
}

variable "lock_table_name" {
  description = "The name of the DynamoDB table to use for the backend"
  default     = "terraform-state-lock-mlops-bootcamp"
}
