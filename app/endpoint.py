import os

HOSTNAME = os.getenv("LOCALSTACK_HOSTNAME")
PORT = os.getenv("EDGE_PORT")

endpoint_url = f"http://{HOSTNAME}:{PORT}"