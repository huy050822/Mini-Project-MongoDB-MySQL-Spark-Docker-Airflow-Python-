from typing import Optional, List, Dict
from config.logging_config import get_logger
from pyspark.sql import SparkSession
from pyspark.sql.types import *

logger = get_logger("Spark_config", "spark_connect.log")

class Spark_connect():
    def __init__(
        self,
        app_name : str,
        master_url : str = "local[*]",
        executor_memory : Optional[str] = "4g",
        executor_cores: Optional[int] = 2 ,
        driver_memory : Optional[str] = '2g',
        num_executors : Optional[int] = 1,
        jar_packages : Optional[List[str]] = None ,
        spark_conf : Optional[Dict[str,str]] = None
        ):

        self.app_name = app_name
        self.master_url = master_url
        self.executor_memory = executor_memory
        self.executor_cores = executor_cores
        self.driver_memory = driver_memory
        self.num_executors = num_executors
        self.jar_packages = jar_packages or [
            "com.mysql:mysql-connector-j:8.3.0",
            "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"
        ]
        self.spark_conf = spark_conf

    def spark_session(self) -> SparkSession:
        try:
            logger.info("Starting Spark session")
            builder = SparkSession.builder.appName(self.app_name).master(self.master_url)

            if self.executor_memory:
                #config executor memory
                builder = builder.config("spark.executor.memory", self.executor_memory)
                
            if self.executor_cores:
                #config executor cores
                builder = builder.config("spark.executor.cores", str(self.executor_cores))
                
            if self.driver_memory:
                #config driver memory
                builder = builder.config("spark.driver.memory", self.driver_memory)
                
            if self.num_executors:
                #config executors
                builder = builder.config("spark.executor.instances", str(self.num_executors))
            
            # ["driver_mongo.jar", "driver_mysql.jar"] -> "driver_mongo.jar,driver_mysql.jar"

            if self.jar_packages:
                jar_packages = ",".join(self.jar_packages)
                #config jar packages
                builder =  builder.config("spark.jars.packages", jar_packages)
                logger.info(f"Used packages {jar_packages}")
            
            #For another key value spark configs 
            if self.spark_conf:
                for key, value in self.spark_conf.items():
                    builder = builder.config(key,value)
            
            spark = builder.getOrCreate()
            
            logger.info("Initialized Spark Session")
            return spark        
        except Exception as e:
            logger.error(f"Failed to connect Spark : {str(e)}")
            raise e
    

# from pyspark.sql.types import *

# def main():
#     spark_connect = Spark_connect(
#         app_name= "huy",
#         master_url= "local[*]",
#         executor_memory= '5g',
#         executor_cores= 1,
#         driver_memory= "1g",
#         num_executors= 1,

#     )
#     data = [
#         ("Huy", 30, "Newyork"),
#         ("Min", 35, "LA"),
#         ("Hn", 19, "Cali")
#     ]

#     schema = StructType([
#         StructField("Name", StringType(), True),
#         StructField("Age", IntegerType(), True),
#         StructField("City", StringType(), True)

#     ])  
#     spark = spark_connect.spark_session()

#     df = spark.createDataFrame(data, schema)

#     print(df.show())
# if __name__ == "__main__":
#     main()