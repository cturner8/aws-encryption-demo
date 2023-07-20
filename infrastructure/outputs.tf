output "files_bucket_arn" {
  value = aws_s3_bucket.files_bucket.arn
}

output "encrypt_key_arn" {
  value = aws_kms_key.encrypt_key.arn
}