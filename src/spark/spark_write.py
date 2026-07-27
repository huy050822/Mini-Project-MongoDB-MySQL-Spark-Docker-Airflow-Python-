from typing import Dict
from pyspark.sql import SparkSession, DataFrame
from config.logging_config import get_logger

logger1 = get_logger("Spark_write_mysql", "spark_write.log")
logger2 = get_logger("Spark_write_mongodb", "spark_write.log")
class Spark_Write_MySql:

    def __init__(self, spark: SparkSession, mysql_config: Dict):
        self.spark = spark
        self.mysql_config = mysql_config

    def spark_write_mysql(self, df_to_write: DataFrame, mysql_table: str, mode : str):
        cfg = self.mysql_config
        #Use dataclass so notice about cfg.host not cfg["host"]
        jdbc_url = f"jdbc:mysql://{cfg.host}:{cfg.port}/{cfg.database}" 

        #Config 
        logger1.info("Spark starting write to Mysql")
        df_to_write.write \
        .format("jdbc")\
        .mode(mode) \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("url", jdbc_url) \
        .option("dbtable", mysql_table) \
        .option("user", cfg.user) \
        .option("password", cfg.password)\
        .save()
        
        logger1.info("Spark wrote to Mysql successfully")

class Spark_Write_Mongodb:
    def __init__(self, spark:SparkSession, mongodb_config: Dict):
        self.spark = spark
        self.mongodb_config = mongodb_config

    def spark_write_mongodb(self, df_to_write_mongodb: DataFrame , collection_name : str, mode:str ):
    
            config = self.mongodb_config
            #Check objective from database_config.py in config folder
            if hasattr(config, "user") and config.user and config.password:
                mongo_uri = f"mongodb://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}?authSource=admin"
            else:
                mongo_uri = f"mongodb://{config.host}:{config.port}/{config.database}"
            logger2.info("Spark starting write to Mongodb")
            writer = df_to_write_mongodb.write\
                .format("mongodb") \
                .mode(mode)\
                .option("connection.uri", mongo_uri)\
                .option("database", config.database)\
                .option("collection", collection_name)\

            #Error Mongodb 10.3.0 , cannot use mode append with operationType and upsertDocument
            if mode == "overwrite":
                 writer = writer\
                    .option("operationType", "replace") \
                    .option("upsertDocument", "true")

            writer.save()


                 
            logger2.info("Spark wrote to Mongodb successfully")
            
