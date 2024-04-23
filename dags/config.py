import os
from dotenv import load_dotenv

load_dotenv()

environment = {
    "INFLUXDB_TOKEN": os.getenv("INFLUXDB_TOKEN"),
    "INFLUXDB_ORG": os.getenv("INFLUXDB_ORG"),
    "INFLUXDB_URL": os.getenv("INFLUXDB_URL"),
    "REFRESH_RATE": os.getenv("REFRESH_RATE"),
}
