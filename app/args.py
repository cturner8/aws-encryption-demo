import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-l",
    "--log",
    default="warning",
    help="Provide logging level. Example --log debug, default=warning",
)

args = parser.parse_args()
