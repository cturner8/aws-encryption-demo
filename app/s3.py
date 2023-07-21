from logger import logger

import os
import pathlib
import tempfile

import localstack_client.session as boto3
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")

def get_file(file_name, bucket):
    """Get a file from an S3 bucket

    :param file_name: File to read
    :param bucket: Bucket to read from
    :return: File if found, else None
    """

    logger.info("Getting file %s from %s", file_name, bucket)

    with tempfile.TemporaryDirectory() as tmpdirname:
        print("Created temporary directory", tmpdirname)

    output_file_path = f"{tmpdirname}/{file_name}"

    try:
        pathlib.Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file_path, 'wb') as file:
            s3_client.download_fileobj(bucket, file_name, file)
    except ClientError as e:
        logger.error(e)
        return None

    logger.info("Read file %s to %s", file_name, output_file_path)

    return file

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    logger.info("Uploading file %s to %s", file_name, bucket)

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logger.error(e)
        return False
    
    logger.info("Uploaded file to %s", object_name)

    return True