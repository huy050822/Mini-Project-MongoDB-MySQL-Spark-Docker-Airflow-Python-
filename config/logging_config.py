import logging 
import os 
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# logging.basicConfig(
    #     filename="database.log",
    #     level=logging.INFO,
    #     format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    #     encoding="utf-8",
    #     force=True
    # )


#Create folder log
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True) #Check folder exist, if not => create
FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s" #Set format

#Config
HANDLER_CONFIG = {
    "rotating" : {
        "class": RotatingFileHandler,
        "kwargs" : {
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "encoding" : "utf-8"
        }
    },
    "timed": {
        "class" : TimedRotatingFileHandler,
        "kwargs" : {
            "when": "midnight",
            "interval" : 1,
            "backupCount": 5,
            "encoding" : "utf-8"
        }
    }
}

#Set handler
def set_up_handler(file, handler_type = "rotating"): #default = rotating
    config = HANDLER_CONFIG[handler_type]
    formatter = logging.Formatter(FORMAT)
    
    handler = config["class"](
        os.path.join(LOG_DIR, file),
        **config["kwargs"]
    )
    
    handler.setFormatter(formatter)
    return handler

#Write logs
def get_logger(name, file, handler_type = "rotating", level=logging.INFO):
    #Set up logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logger.handlers:
        return logger
    #Create a rotating handler
    # file_handler = RotatingFileHandler(
    #     os.path.join(LOG_DIR, file),
    #     maxBytes= 5 * 1024 * 1024, #Use byte => 1mb = 1024KByte * 1024byte
    #     backupCount= 5,
    #     encoding="utf-8"
    # )
    # formatter = logging.Formatter(FORMAT)
    # file_handler.setFormatter(formatter)

    handler = set_up_handler(file, handler_type)
    logger.addHandler(handler)
    return logger
    
    
