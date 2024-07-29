resource "aws_iam_user" "dev_user" {
  for_each = toset(var.users)

  name = each.key
  
  tags = {
    Name = "Developer User: ${each.key}"
  }
}

