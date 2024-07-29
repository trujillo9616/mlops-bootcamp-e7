variable "region" {
  description = "The AWS region for deploying the infrastructure"
  type        = string
  default     = "us-east-2"
}

variable "bucket_name" {
  description = "The name of the S3 buckets to store the datasets and artifacts"
  type        = string
  default     = "mlops-bootcamp-datalake"
}
