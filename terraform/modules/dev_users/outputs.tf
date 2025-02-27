output "user_names" {
  description = "List of IAM user names"
  value       = [for user in aws_iam_user.dev_user : user.name]
}

output "group_name" {
  description = "Name of the group to add users to"
  value       = aws_iam_group.dev_group.name
}
