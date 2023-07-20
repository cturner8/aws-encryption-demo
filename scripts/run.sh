
kms_key_id=$(tflocal -chdir=infrastructure output -raw encrypt_key_arn)

export KMS_KEY_ID=${kms_key_id}

python3 app/main.py -l info