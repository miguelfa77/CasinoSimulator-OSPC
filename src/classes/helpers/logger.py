import logging
import os

LOG_FOLDER = ".logs"

def myLogger() -> logging.Logger:

    file_name = "log_file.log"
    logger = logging.getLogger(file_name)

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)
    
        file_handler = logging.FileHandler(f"{LOG_FOLDER}/{file_name}", mode="w")
        file_format = logging.Formatter(
                "%(asctime)s - %(thread)s - %(levelname)s - %(message)s"
            )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_format)

        logger.addHandler(console_handler)

        return logger