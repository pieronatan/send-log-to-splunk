resource "aws_iam_role" "main" {
  name               = format("%s-lambda", var.project)
  tags               = var.tags
  assume_role_policy = data.aws_iam_policy_document.lambda_role.json
}

resource "aws_iam_role_policy" "main" {
  name   = format("%s-lambda", var.project)
  role   = aws_iam_role.main.id
  policy = data.aws_iam_policy_document.lambda_policy.json
}
