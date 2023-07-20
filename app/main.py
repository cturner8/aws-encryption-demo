import kms
import logging
import env
from args import args

logging.basicConfig(level=args.log.upper())


def main():
    logging.info("Starting")

    encrypted = kms.encrypt_file("./files/test.txt", env.KMS_KEY_ID)

    logging.info("Encrypted: %s", encrypted)

    if encrypted == True:
        decrypted = kms.decrypt_file("./files/test.txt")

        logging.info("Decrypted: %s", decrypted)

    logging.info("Done")


if __name__ == "__main__":
    main()
