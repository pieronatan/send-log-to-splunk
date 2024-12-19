########
#GLOBAL#
########

variable "project" {
  default = "send-logs"
}

variable "tags" {
  default = {
    Product = "send-logs"
  }
}

variable "region" {
  default = {
    dev  = "us-east-1"
  }
}

variable "environment" {
  type = string
}

variable "s3_bucket" {
  default = {
    dev  = "bucket-logs-dev"
  }
}

variable "vpc_name" {
  default = "default"
}
