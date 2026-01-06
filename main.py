from databases.mysql_connect import MySQLConnect
from config.database_config import get_database_config
from databases.mongodb_connect import MongoDB_connect
from config.logging_config import get_logger

#main function
def main(config):
    #Start logger
    logger = get_logger("main", "app.log")
    logger.info("Starting application")
    
    #Connect MySQL
    with MySQLConnect(config["mysql"].host, config["mysql"].port, config["mysql"].user, config["mysql"].password, config["mysql"].database) as Mysql_client:
        Mysql_client.connector()
        #Connect MongoDB
    with MongoDB_connect(config["mongodb"].uri, config["mongodb"].database) as MongoDB_client:
        MongoDB_client.connector()

    logger.info("End App")

if __name__ == "__main__":
    config = get_database_config()
    main(config)