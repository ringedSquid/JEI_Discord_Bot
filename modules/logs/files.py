import os

#If a critical error happens, save the log file
def stash_log(path: str) -> None:
    if (os.path.exists(path + "/log0.log")):
        os.rename(path + "/log0.log", path + "/log1.log")
