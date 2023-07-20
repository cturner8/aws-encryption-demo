import kms
import logging
import os
import argparse

KMS_KEY_ID = os.getenv("KMS_KEY_ID")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-l",
    "--log",
    default="warning",
    help="Provide logging level. Example --log debug, default=warning",
)

args = parser.parse_args()

logging.basicConfig(level=args.log.upper())


def main():
    logging.info("Starting")
    kms.create_data_key(KMS_KEY_ID)

    encrypted = kms.encrypt_file("./files/test.txt", KMS_KEY_ID)

    logging.info("Encrypted: %s", encrypted)

    if encrypted == True:
        decrypted = kms.decrypt_file("./files/test.txt")

        logging.info("Decrypted: %s", decrypted)

    logging.info("Done")


if __name__ == "__main__":
    main()
