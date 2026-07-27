from databases.mysql_connect import MySQLConnect
from config.database_config import get_database_config
from databases.mongodb_connect import MongoDB_connect
from config.logging_config import get_logger
from databases.schema_manager import create_mysql_schema, create_mongodb_schema
from config.spark_config import Spark_connect



#main function
def main(config):
    #Start logger
    logger = get_logger("main", "app.log")
    logger.info("Starting application")
    
    #Connect MySQL
    logger.info("Connect to Mysql")
    with MySQLConnect(config["mysql"].host, config["mysql"].port, config["mysql"].user, config["mysql"].password, config["mysql"].database) as Mysql_client:
        connection , cursor = Mysql_client.connector()
        create_mysql_schema(connection,cursor, config["mysql"].database)
        #Connect MongoDB
    logger.info("Connect to Mongodb")
    with MongoDB_connect(config["mongodb"].uri, config["mongodb"].database) as MongoDB_client:
        client = MongoDB_client.connector()
        create_mongodb_schema(client,config["mongodb"].database)
    
    logger.info("Connect to Spark")
    
    spark_connect_main = Spark_connect(
        app_name= "Data Transfer",
        master_url= "local[*]",
        executor_cores= 2,
        executor_memory= "4g"
        jar_packages= drivers
    )


    logger.info("End App")

if __name__ == "__main__":
    config = get_database_config()
    main(config)