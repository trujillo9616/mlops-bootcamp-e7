resource "random_id" "datalake_name" {
  byte_length = 8
  prefix      = var.bucket_name
}

module "s3_bucket_datalake" {
  source      = "../modules/s3"
  bucket_name = random_id.datalake_name.hex
}
