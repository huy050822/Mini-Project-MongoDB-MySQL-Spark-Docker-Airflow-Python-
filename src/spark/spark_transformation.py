from config.spark_config import Spark_connect
from pyspark.sql import *
from src.spark.spark_write import Spark_Write_MySql
from src.spark.spark_write import Spark_Write_Mongodb
from src.spark.spark_read import Spark_Read_Mongodb
from pyspark.sql.types import *
from config.database_config import get_database_config
from src.spark.spark_clean import Data_clean
from config.logging_config import get_logger

logger = get_logger("Spark_ETL", "ETL_pipeline.log")

class ETL_pipeline:
    def __init__(self):


        spark_connect = Spark_connect(
            app_name= "huy",
            master_url= "local[*]",
            executor_memory= '5g',
            executor_cores= 1,
            driver_memory= "1g",
            num_executors= 1,
            jar_packages= ["com.mysql:mysql-connector-j:8.3.0",
                "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0"
            ]
        )

        self.spark = spark_connect.spark_session()
        self.dtb_config = get_database_config()

        self.mongodb_read = Spark_Read_Mongodb(self.spark, self.dtb_config["mongodb"])
        self.mongodb_write = Spark_Write_Mongodb(self.spark, self.dtb_config["mongodb"])
        self.mysql_write = Spark_Write_MySql(self.spark, self.dtb_config["mysql"])

        self.cleaner = Data_clean(self.spark)


    def pipeline_exc(self, file_path:str, mongo_collection= "events", mysql_table = "github_event"):

        try:
            #Read file json by spark
            
            logger.info(f"Reading from file path {file_path}")
            df_file_raw = self.spark.read \
                .json(file_path)     

            # df_file_raw.show(5)

            #Write to mongodb from json
            logger.info(f"Writing raw data into Mongodb: {mongo_collection}")
            self.mongodb_write.spark_write_mongodb(
                df_to_write_mongodb= df_file_raw,
                collection_name= mongo_collection,
                mode= "append"
            )

            #Clean data raw (staying in mongodb)
            logger.info("Get data from Mongodb & Processing raw data")
            df_mongo_raw = self.mongodb_read.spark_read_mongodb(
                collection_name=mongo_collection
            )
            logger.info("Processing raw data from MongoDB")
            df_actors, df_repos, df_orgs, df_events = self.cleaner.clean_data(df_mongo_raw)


            # df_clean.show(10)
            
            logger.info(f"Write processed data into Mysql {mysql_table}")
            #Write cleaned data to 

            self.mysql_write.spark_write_mysql(
                df_actors, mysql_table="actors", mode="append"
            )
            self.mysql_write.spark_write_mysql(
                df_repos, mysql_table="repositories", mode="append"
            )
            self.mysql_write.spark_write_mysql(
                df_orgs, mysql_table="organizations", mode="append"
            )

            self.mysql_write.spark_write_mysql(
                df_events, mysql_table="github_events", mode="append"
            )

        except Exception as e:

            raise e


if __name__ == "__main__":

    pipeline = ETL_pipeline()


    json_path = "/opt/airflow/data/2015-03-01-0.json"



    pipeline.pipeline_exc(
        file_path= json_path,
        mongo_collection="events",
        mysql_table="github_events",
    )








# data = [
#         ("Huy", 30, "Newyork"),
#         ("Min", 35, "LA"),
#         ("Hn", 19, "Cali") 
# ] 

# schema = StructType([
#         StructField("Name", StringType(), True),
#         StructField("Age", IntegerType(), True),
#         StructField("City", StringType(), True)
# ])


# spark = spark_connect.spark_session()

# try:
#     print("---> [1] TAO DATAFRAME...")
#     df = spark.createDataFrame(data, schema)

#     print("---> [2] LAY CONFIG MYSQL...")
#     dtb_config = get_database_config()
#     mysql_config = dtb_config["mysql"]

#     print("---> [3] KHOI TAO WRITER...")
#     writer = Spark_Write_MySql(spark, mysql_config)

#     print("---> [4] THUC HIEN GHI VAO MYSQL...")
#     writer.spark_write(df, mysql_table="dtb", mode="append")

#     print("---> [5] THANH CONG HOAN TOAN!")

# except Exception as e:
#     print("Error")
