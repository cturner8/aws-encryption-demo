resource "aws_kms_key" "encrypt_key" {
  key_usage = "ENCRYPT_DECRYPT"
}
