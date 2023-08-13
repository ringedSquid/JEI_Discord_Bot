import os
from pathlib import Path

LOG_PATH = f"{Path(__file__).parent.parent.parent}/etc/logs"

#If a critical error happens, save the log file
def stash_log() -> None:
    if (os.path.exists(f"{LOG_PATH}/log0.log")):
        os.rename(f"{LOG_PATH}/log0.log", f"{LOG_PATH}/log1.log")
