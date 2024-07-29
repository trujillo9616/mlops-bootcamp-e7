resource "aws_iam_group" "dev_group" {
  name = var.user_group_name
}

resource "aws_iam_user_group_membership" "dev_user_group_membership" {
  for_each = toset(var.users)

  user = aws_iam_user.dev_user[each.key].name
  groups = [aws_iam_group.dev_group.name]
}
