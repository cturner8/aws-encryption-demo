output "files_bucket_arn" {
  value = aws_s3_bucket.files_bucket.arn
}

output "encrypt_key_arn" {
  value = aws_kms_key.encrypt_key.arn
}

output "api_id" {
  value = aws_api_gateway_rest_api.api.id
}

output "api_url" {
  value = aws_api_gateway_stage.api_stage.invoke_url
}
