variable "lambda_timeout" {
  type    = number
  default = 30
}

variable "lambda_memory" {
  type    = number
  default = 256
}

resource "aws_lambda_function" "prime_number" {
  filename         = data.archive_file.lambda.output_path
  function_name    = "count_primes"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/LambdaBasicExecutionRole"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"

  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory

  source_code_hash = data.archive_file.lambda.output_base64sha256
}
