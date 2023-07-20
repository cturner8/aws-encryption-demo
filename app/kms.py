import logging
import base64
from cryptography.fernet import Fernet

import localstack_client.session as boto3
from botocore.exceptions import ClientError

kms_client = boto3.client("kms")

NUM_BYTES_FOR_LEN = 36


def create_data_key(cmk_id, key_spec="AES_256"):
    """Generate a data key to use when encrypting and decrypting data

    :param cmk_id: KMS CMK ID or ARN under which to generate and encrypt the
    data key.
    :param key_spec: Length of the data encryption key. Supported values:
        'AES_128': Generate a 128-bit symmetric key
        'AES_256': Generate a 256-bit symmetric key
    :return Tuple(EncryptedDataKey, PlaintextDataKey) where:
        EncryptedDataKey: Encrypted CiphertextBlob data key as binary string
        PlaintextDataKey: Plaintext base64-encoded data key as binary string
    :return Tuple(None, None) if error
    """
    logging.info("Creating data key")

    # Create data key
    try:
        response = kms_client.generate_data_key(KeyId=cmk_id, KeySpec=key_spec)
    except ClientError as e:
        logging.error(e)
        return None, None

    logging.info("Created new AWS KMS data key")

    # Return the encrypted and plaintext data key
    return response["CiphertextBlob"], base64.b64encode(response["Plaintext"])


def encrypt_file(filename, cmk_id):
    """Encrypt a file using an AWS KMS CMK

    A data key is generated and associated with the CMK.
    The encrypted data key is saved with the encrypted file. This enables the
    file to be decrypted at any time in the future and by any program that
    has the credentials to decrypt the data key.
    The encrypted file is saved to <filename>.encrypted
    Limitation: The contents of filename must fit in memory.

    :param filename: File to encrypt
    :param cmk_id: AWS KMS CMK ID or ARN
    :return: True if file was encrypted. Otherwise, False.
    """

    # Read the entire file into memory
    try:
        with open(filename, "rb") as file:
            file_contents = file.read()
    except IOError as e:
        logging.error(e)
        return False

    # Generate a data key associated with the CMK
    # The data key is used to encrypt the file. Each file can use its own
    # data key or data keys can be shared among files.
    # Specify either the CMK ID or ARN
    data_key_encrypted, data_key_plaintext = create_data_key(cmk_id)
    if data_key_encrypted is None:
        return False

    logging.info("Encrypting file: %s", filename)

    # Encrypt the file
    f = Fernet(data_key_plaintext)
    file_contents_encrypted = f.encrypt(file_contents)

    # Write the encrypted data key and encrypted file contents together
    encrypted_filename = filename + ".encrypted"

    try:
        with open(encrypted_filename, "wb") as file_encrypted:
            file_encrypted.write(
                len(data_key_encrypted).to_bytes(NUM_BYTES_FOR_LEN, byteorder="big")
            )
            file_encrypted.write(data_key_encrypted)
            file_encrypted.write(file_contents_encrypted)
    except IOError as e:
        logging.error(e)
        return False

    logging.info("File encrypted: %s", encrypted_filename)

    # For the highest security, the data_key_plaintext value should be wiped
    # from memory. Unfortunately, this is not possible in Python. However,
    # storing the value in a local variable makes it available for garbage
    # collection.
    return True


def decrypt_data_key(data_key_encrypted):
    """Decrypt an encrypted data key

    :param data_key_encrypted: Encrypted ciphertext data key.
    :return Plaintext base64-encoded binary data key as binary string
    :return None if error
    """

    logging.info("Decrypting data key")

    # Decrypt the data key
    try:
        response = kms_client.decrypt(CiphertextBlob=data_key_encrypted)
    except ClientError as e:
        logging.error(e)
        return None

    logging.info("Data key decrypted")

    # Return plaintext base64-encoded binary data key
    return base64.b64encode((response["Plaintext"]))


def decrypt_file(filename):
    """Decrypt a file encrypted by encrypt_file()

    The encrypted file is read from <filename>.encrypted
    The decrypted file is written to <filename>.decrypted

    :param filename: File to decrypt
    :return: True if file was decrypted. Otherwise, False.
    """

    logging.info("Decrypting file: %s", filename)

    # Read the encrypted file into memory
    try:
        with open(filename + ".encrypted", "rb") as file:
            file_contents = file.read()
    except IOError as e:
        logging.error(e)
        return False

    # The first NUM_BYTES_FOR_LEN bytes contain the integer length of the
    # encrypted data key.
    # Add NUM_BYTES_FOR_LEN to get index of end of encrypted data key/start
    # of encrypted data.
    data_key_encrypted_len = (
        int.from_bytes(file_contents[:NUM_BYTES_FOR_LEN], byteorder="big")
        + NUM_BYTES_FOR_LEN
    )
    data_key_encrypted = file_contents[NUM_BYTES_FOR_LEN:data_key_encrypted_len]

    # Decrypt the data key before using it
    data_key_plaintext = decrypt_data_key(data_key_encrypted)
    if data_key_plaintext is None:
        return False

    # Decrypt the rest of the file
    f = Fernet(data_key_plaintext)
    file_contents_decrypted = f.decrypt(file_contents[data_key_encrypted_len:])

    # Write the decrypted file contents
    decrypted_filename = filename + ".decrypted"
    try:
        with open(filename + ".decrypted", "wb") as file_decrypted:
            file_decrypted.write(file_contents_decrypted)
    except IOError as e:
        logging.error(e)
        return False

    logging.info("File decrypted: %s", decrypted_filename)

    # The same security issue described at the end of encrypt_file() exists
    # here, too, i.e., the wish to wipe the data_key_plaintext value from
    # memory.
    return True
