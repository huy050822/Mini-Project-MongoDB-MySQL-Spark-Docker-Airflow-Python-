import os 
from typing import Dict
from config.logging_config import get_logger
from pyspark.sql import *

logger1 = get_logger("Spark_read_from_Mongodb", "spark_read.log")
logger2 = get_logger("Spark_read_from_json", "spark_read.log")
class Spark_reader:
    def __init__(self, spark:SparkSession, mongodb_config : Dict):

        self.spark = spark
        self.mongodb_config = mongodb_config

    def spark_read_json(self, file : str):
        if not os.path.exists(file):
            logger2.error(f"Not found file {file}")
            raise FileNotFoundError
        
        try:
            df = self.spark.read.json(file)
            logger2.info(f"Spark read {file} completely")
            return df
        except Exception as e:
            logger2.info(f"Error reading JSON file {file} with Spark: {str(e)}")
            raise e 


    def spark_read_mongodb(self, collection_name = str ):

        config = self.mongodb_config

        #Check objective from database_config.py in config folder
        if hasattr(config, "user") and config.user and config.password:
            mongo_uri = f"mongodb://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}?authSource=admin"
        else:
            mongo_uri = f"mongodb://{config.host}:{config.port}/{config.database}"


        logger1.info("Spark starting read Mongodb")
        self.spark.read\
            .format("mongodb") \
            .option("connection.uri", mongo_uri)\
            .option("database", config.database)\
            .option("collection", collection_name)\
            .load()

        logger1.info("Spark read from Mongodb successfully")
        
        
        
