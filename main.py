from config.logging_config import set_up_logging
from databases.mysql_connect import MySQLConnect
from config.database_config import get_database_config
import logging


#main function
def main(config):
    #Start logger
    logger = logging.getLogger(__name__)
    logger.info("Starting application")
    
    #Connect MySQL
    mysql = MySQLConnect(config["mysql"].host, config["mysql"].port, config["mysql"].user, config["mysql"].password, config["mysql"].database)
    con, cursor = mysql.connector()
    if not con:
        logger.error("Database connection failed")
        return
    logger.info("Database connection OK")
    mysql.close()



if __name__ == "__main__":
    set_up_logging() 
    config = get_database_config()
    main(config)