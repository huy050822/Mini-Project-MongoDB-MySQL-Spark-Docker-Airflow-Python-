from config.spark_config import Spark_connect
from pyspark.sql import *
from src.spark.spark_write_mysql import Spark_Write_MySql
from pyspark.sql.types import *
from config.database_config import get_database_config


spark_connect = Spark_connect(
    app_name= "huy",
    master_url= "local[*]",
    executor_memory= '5g',
    executor_cores= 1,
    driver_memory= "1g",
    num_executors= 1,
    jar_packages= ["com.mysql:mysql-connector-j:8.3.0"]
)

data = [
        ("Huy", 30, "Newyork"),
        ("Min", 35, "LA"),
        ("Hn", 19, "Cali") 
] 

schema = StructType([
        StructField("Name", StringType(), True),
        StructField("Age", IntegerType(), True),
        StructField("City", StringType(), True)
])


spark = spark_connect.spark_session()

df = spark.createDataFrame(data, schema)

dtb_config = get_database_config()
mysql_config = dtb_config["mysql"]

writer = Spark_Write_MySql(spark, mysql_config)

df_writer = writer.spark_write(df, mysql_table="dtb", mode="append")

print(">>> PHIEN CHAY DA HOAN THANH <<<")