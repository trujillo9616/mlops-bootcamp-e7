resource "aws_iam_policy" "dev_policy" {
  name        = var.custom_policy_name
  description = "A custom policy for the dev group"
  policy      = data.aws_iam_policy_document.custom_policy_document.json
}

resource "aws_iam_policy_attachment" "dev_policy_attachment" {
  name       = var.custom_policy_name
  policy_arn = aws_iam_policy.dev_policy.arn
  groups     = [aws_iam_group.dev_group.name]
}

locals {
  policy_statements = [
    for statement in var.policy_statements : {
      effect    = statement.effect
      actions   = statement.actions
      resources = statement.resources
    }
  ]
}

data "aws_iam_policy_document" "custom_policy_document" {
  dynamic "statement" {
    for_each = local.policy_statements

    content {
      effect   = statement.value.effect
      actions   = statement.value.actions
      resources = statement.value.resources
    }
  }
}
