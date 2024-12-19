resource "aws_security_group" "main" {
  name   = var.project
  tags   = var.tags
  vpc_id = data.aws_vpc.for_lambda.id
}

resource "aws_security_group_rule" "egress" {
  type              = "egress"
  to_port           = 0
  protocol          = -1
  from_port         = 0
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.main.id
}
