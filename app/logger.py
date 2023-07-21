import logging
from args import args

logging.basicConfig(level=args.log.upper())
logger = logging.getLogger("aws_encryption_demo")