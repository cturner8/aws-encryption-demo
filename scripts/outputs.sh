
kms_key_id=$(tflocal -chdir=infrastructure output -raw encrypt_key_arn)
bucket_arn=$(tflocal -chdir=infrastructure output -raw files_bucket_arn)

export KMS_KEY_ID=${kms_key_id}
export BUCKET_ARN=${bucket_arn}

echo "KMS_KEY_ID=${kms_key_id}" > .env
echo "BUCKET_ARN=${bucket_arn}" >> .env