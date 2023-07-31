import os

#If a critical error happens, save the log file
def stash_log(path: str) -> None:
    if (os.path.exists(f"{path}/log0.log")):
        os.rename(f"{path}/log0.log", f"{path}/log1.log")
