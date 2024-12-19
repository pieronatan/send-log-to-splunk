data "aws_iam_policy_document" "lambda_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "ec2:CreateNetworkInterface",
      "ec2:Describe*",
      "ec2:DeleteNetworkInterface"
    ]
    resources = ["*"]
  }

  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["*"]
  }

  statement {
    actions = [
      "s3:GetBucketLocation",
      "s3:GetObject*",
      "s3:GetObjectVersion",
      "s3:ListBucket",
      "s3:PutObject*"
    ]
    resources = ["*"]
  }
}

data "aws_vpc" "for_lambda" {
  filter {
    name   = "tag:Name"
    values = [var.vpc_name]
  }
}

resource "null_resource" "install_dependencies" {
  provisioner "local-exec" {
    command = "pip install --upgrade pip && pip install -r ../requirements.txt -t ../"
  }

  triggers = {
    handler_py_checksum        = filemd5("../src/handler.py")
    log_processor_py_checksum  = filemd5("../src/log_processor.py")
    logger_py_checksum         = filemd5("../src/logger.py")
    splunk_manager_py_checksum = filemd5("../src/splunk_manager.py")
    utils_py_checksum          = filemd5("../src/utils.py")
  }
}

data "archive_file" "lambda_function" {
  type = "zip"
  excludes = [
    ".tf",
    ".github",
    "Makefile",
    "README.md",
    "atlantis.yaml",
    "requirements.txt"
  ]
  source_dir  = "../"
  depends_on  = [null_resource.install_dependencies]
  output_path = "./lambda.zip"
}
