import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument( '-l',
                     '--log',
                     default='warning',
                     help='Provide logging level. Example --log debug, default=warning' )

args = parser.parse_args()

logger = logging.getLogger("aws_encryption_demo")
logger.setLevel(args.log.upper())