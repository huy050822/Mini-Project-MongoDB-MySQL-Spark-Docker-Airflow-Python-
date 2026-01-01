from config.logging_config import set_up_logging
from databases.mysql_connect import MySQLConnect
from config.database_config import get_database_config
from databases.mongodb_connect import MongoDB_connect
import logging


#main function
def main(config):
    #Start logger
    logger = logging.getLogger(__name__)
    logger.info("Starting application")
    
    #Connect MySQL
    with MySQLConnect(config["mysql"].host, config["mysql"].port, config["mysql"].user, config["mysql"].password, config["mysql"].database) as Mysql_client:
        Mysql_client.connector()
    logger.info("AFTER MYSQL")
    #Connect MongoDB
    with MongoDB_connect(config["mongodb"].uri, config["mongodb"].database) as MongoDB_client:
        MongoDB_client.connector()

if __name__ == "__main__":
    set_up_logging() 
    config = get_database_config()
    main(config)