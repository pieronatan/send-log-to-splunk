resource "aws_cloudwatch_log_group" "main" {
  name = "/aws/lambda/${var.project}"
  tags = var.tags
}
