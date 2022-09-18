import os

DEBUG = os.getenv("DEBUG", False)
LOG_LOCATION = os.getenv("LOG_LOCATION", "/tmp/log.txt")

def log(data):
    if DEBUG:
        with open(LOG_LOCATION, "a") as f:
            f.writelines("\n" + str(data) + "\n")
