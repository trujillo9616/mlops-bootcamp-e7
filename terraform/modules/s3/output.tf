output "s3_bucket_id" {
  value       = aws_s3_bucket.bucket.id
  description = "The ID of the S3 bucket"
}

output "s3_bucket_name" {
  value       = aws_s3_bucket.bucket.bucket
  description = "The name of the S3 bucket"
}
