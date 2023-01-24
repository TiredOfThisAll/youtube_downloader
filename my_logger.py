from datetime import datetime
import sys, traceback


class MyLogger(object):
    def __init__(self):
        with open('download_logger.txt', 'a') as file:
            pass

    def info(self, exc):
        with open('download_logger.txt', 'a') as file:
            file.write(f"{datetime.utcnow()} INFO: " + exc + '\n')

    def debug(self, exc):
        pass

    def warning(self, exc):
        with open('download_logger.txt', 'a') as file:
            file.write(f"{datetime.utcnow()} WARNING:" + exc + '\n')

    def error(self, exc):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted_lines = traceback.format_exc()
        with open('download_logger.txt', 'a') as file:
            file.write(f"ERROR: {datetime.utcnow()} " + str(exc_type) + str(exc_value) + formatted_lines + '\n')
