from logger import logger

import kms
import s3

import env

FILE_NAME = "test.txt"

def main():
    logger.info("Starting")

    target_file = s3.get_file(FILE_NAME, env.BUCKET_NAME)

    encrypted, encrypted_file = kms.encrypt_file(target_file.name, env.KMS_KEY_ID)

    logger.info("Encrypted: %s", encrypted)

    if encrypted == True:
        s3.upload_file(encrypted_file.name, env.BUCKET_NAME)

        decrypted, decrypted_file = kms.decrypt_file(target_file.name)

        if decrypted == True:
            s3.upload_file(decrypted_file.name, env.BUCKET_NAME)

        logger.info("Decrypted: %s", decrypted)

    logger.info("Done")


if __name__ == "__main__":
    main()
