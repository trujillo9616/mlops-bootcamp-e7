module "dev_users" {
  source = "../modules/dev_users"
  users  = ["ricardo-diaz", "hugo-ramirez"]
  policy_statements = [
    {
      effect  = "Allow"
      actions = ["s3:*"]
      resources = [
        "arn:aws:s3:::${module.s3_bucket_datalake.bucket_name}",
        "arn:aws:s3:::${module.s3_bucket_datalake.bucket_name}/*"
      ]
    }
  ]
}