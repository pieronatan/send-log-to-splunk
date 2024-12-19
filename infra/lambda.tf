resource "aws_lambda_function" "main" {
  description      = "AWS lambda que faz o envio de logs do S3 para o Splunk"
  filename         = data.archive_file.lambda_function.output_path
  function_name    = "send-logs-splunk"
  handler          = "src.handler.handler"
  publish          = true
  role             = aws_iam_role.main.arn
  runtime          = "python3.10"
  source_code_hash = data.archive_file.lambda_function.output_base64sha256
  tags             = var.tags
  timeout          = 300

  environment {
    variables = {
      HTTP_PROXY = "http://proxy.intranet:80"
      NO_PROXY   = ".intranet"

      SPLUNK_HEC_URL   = "http://hec-splunk.intranet:8088/services/collector/event"
      SPLUNK_HEC_TOKEN = "hec_token"
      SPLUNK_HEC_INDEX = "send_logs"
      SOURCE_TYPE_PREFIX = "prefix_send_logs"
    }
  }

  vpc_config {
    subnet_ids         = [
      "subnet-0000000000",
      "subnet-0000000001"
    ]
    security_group_ids = [aws_security_group.main.id]
  }
}

resource "aws_lambda_permission" "logging_permission" {
  action        = "lambda:InvokeFunction"
  principal     = "logs.amazonaws.com"
  source_arn    = "${aws_cloudwatch_log_group.main.arn}:*"
  function_name = aws_lambda_function.main.function_name
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.arn
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${lookup(var.s3_bucket, var.environment)}"
}

resource "aws_s3_bucket_notification" "logs_bucket_notification" {
  bucket = lookup(var.s3_bucket, var.environment)
  lambda_function {
    lambda_function_arn = aws_lambda_function.main.arn
    events              = ["s3:ObjectCreated:*"]
  }
  depends_on = [
    aws_lambda_permission.allow_bucket
  ]
}
