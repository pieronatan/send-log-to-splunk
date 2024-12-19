provider "aws" {
  region  = lookup(var.region, var.environment)
}
