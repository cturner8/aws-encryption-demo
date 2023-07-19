import kms 
import logging
import os 
import argparse

KMS_KEY_ID = os.getenv("KMS_KEY_ID")

parser = argparse.ArgumentParser()
parser.add_argument( '-l',
                     '--log',
                     default='warning',
                     help='Provide logging level. Example --log debug, default=warning' )

args = parser.parse_args()

logging.basicConfig(level=args.log.upper())

def main():
    logging.info("Starting")
    data_key_encrypted, data_key_plaintext = kms.create_data_key(KMS_KEY_ID)

    logging.info("Data key (Encrypted): %s", data_key_encrypted)
    logging.info("Data key (Plaintext): %s", data_key_plaintext)


if __name__ == '__main__':
    main()