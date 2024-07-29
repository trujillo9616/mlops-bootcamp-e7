resource "aws_iam_policy" "dev_policy" {
  name        = var.custom_policy_name
  description = "A custom policy for the dev group"
  path        = "/developers/"
  policy      = data.aws_iam_policy_document.dev_policy[*].json
}

resource "aws_iam_policy_attachment" "dev_policy_attachment" {
  name       = var.custom_policy_name
  policy_arn = aws_iam_policy.dev_policy.arn
  groups     = [aws_iam_group.dev_group.name]
}

locals {
  policy_statement_map = {
    for i, statement in var.policy_statements : i => statement
  }
}

data "aws_iam_policy_document" "dev_policy" {
  for_each = local.policy_statement_map
  
  statement {
    effect = each.value.effect
  
    actions = each.value.actions
    resources = each.value.resources
  }
}
