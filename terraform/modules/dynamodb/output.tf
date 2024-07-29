output "dynamodb_name" {
  value       = aws_dynamodb_table.dynamotable.name
  description = "The name of the DynamoDB table"
}

output "dynamodb_id" {
  value       = aws_dynamodb_table.dynamotable.id
  description = "The ID of the DynamoDB table"
}

output "dynamodb_arn" {
  value       = aws_dynamodb_table.dynamotable.arn
  description = "The ARN of the DynamoDB table"
}
