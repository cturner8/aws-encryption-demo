
kms_key_id=$(tflocal -chdir=infrastructure output -raw encrypt_key_arn)
bucket_arn=$(tflocal -chdir=infrastructure output -raw files_bucket_arn)
bucket_name=$(tflocal -chdir=infrastructure output -raw files_bucket_name)

export KMS_KEY_ID=${kms_key_id}
export BUCKET_ARN=${bucket_arn}
export BUCKET_NAME=${bucket_name}

echo "KMS_KEY_ID=${kms_key_id}" > .env
echo "BUCKET_ARN=${bucket_arn}" >> .env
echo "BUCKET_NAME=${bucket_name}" >> .env

echo "Outputs written to .env file"