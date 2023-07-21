resource "aws_api_gateway_rest_api" "api" {
  name = "files"
  tags = {
    "_custom_id_" = "files"
  }
}

resource "aws_api_gateway_resource" "api_resource" {
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "api"
  rest_api_id = aws_api_gateway_rest_api.api.id
}


resource "aws_api_gateway_deployment" "api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.api_resource.id,
      aws_api_gateway_method.api_get.id,
      aws_api_gateway_integration.api_get_integration.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_method" "api_get" {
  authorization = "NONE"
  http_method   = "GET"
  resource_id   = aws_api_gateway_resource.api_resource.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_integration" "api_get_integration" {
  http_method = aws_api_gateway_method.api_get.http_method
  resource_id = aws_api_gateway_resource.api_resource.id
  rest_api_id = aws_api_gateway_rest_api.api.id
  type        = "MOCK"
}


resource "aws_api_gateway_stage" "api_stage" {
  deployment_id = aws_api_gateway_deployment.api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
  stage_name    = "local"
}
