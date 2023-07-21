resource "aws_lambda_permission" "hello_lambda_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hello_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${local.region}:${local.account_id}:${aws_api_gateway_rest_api.api.id}/*/${aws_api_gateway_method.api_get.http_method}${aws_api_gateway_resource.hello_resource.path}"
}

resource "aws_lambda_function" "hello_lambda" {
  filename      = data.archive_file.hello_lambda_zip.output_path
  function_name = "hello_lambda"
  role          = aws_iam_role.hello_role.arn
  handler       = "handlers/hello.handler"
  runtime       = "python3.10"

  source_code_hash = data.archive_file.hello_lambda_zip.output_base64sha256
}

data "archive_file" "hello_lambda_zip" {
  type             = "zip"
  source_dir       = "${path.module}/../app"
  output_file_mode = "0666"
  output_path      = "${path.module}/archive/hello.zip"

  excludes = ["__pycache__"]
}
