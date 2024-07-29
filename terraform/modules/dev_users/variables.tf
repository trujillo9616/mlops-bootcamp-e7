variable "users" {
  description = "(Required) List of IAM users to create"
  type        = list(string)
}

variable "user_group_name" {
  description = "Name of the group to add users to"
  type        = string
  default     = "dev-group"
}

variable "custom_policy_name" {
  description = "Name of the custom policy to create"
  type        = string
  default     = "dev-policy"
}

variable "policy_statements" {
  description = "(Required) List of policy statements to include in the custom policy"
  type        = list(object({
    effect     = string
    actions    = list(string)
    resources  = list(string)
  }))
}
