import logging
import re

INVALID_CHARS_FILE = '[<>:"\\\/|?*]' 

def remove_invalid(string):
    return re.sub(INVALID_CHARS_FILE, '', string)

def insert_log(text):
    file = './info.log'
    format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    infoLog = logging.FileHandler(file)
    infoLog.setFormatter(format)

    logger = logging.getLogger(file)
    logger.setLevel(logging.WARNING)
    
    if not logger.handlers:
        logger.addHandler(infoLog)
        logger.warning(text)
    
    infoLog.close()
    logger.removeHandler(infoLog)
