from config.logging_config import get_logger
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, BooleanType
from config.spark_config import Spark_connect
from src.spark.spark_write import Spark_Write_Mongodb
from config.database_config import Mongodb_Config

# Cấu hình logging
logger = get_logger("TestMongoDB", "app.log")

def test_mongo_pipeline():
    logger.info("STEP 1: Starting Spark Session...")
    # SỬA TẠI ĐÂY: Truyền 'app_name' vào hàm khởi tạo Spark_connect
    spark_builder = Spark_connect(app_name="Test_MongoDB_Pipeline")
    spark = spark_builder.spark_session()
    
    logger.info("STEP 2: Preparing MongoDB config...")
    mongo_config = Mongodb_Config(
        uri="mongodb://localhost:27017",
        database="github_db",            # Tên database của bạn
        host="localhost",
        port=27017
    )
    
    logger.info("STEP 3: Creating Dummy DataFrame...")
    schema = StructType([
        StructField("_id", IntegerType(), False),  # BSON 'int' (32-bit)
        StructField("login", StringType(), True),
        StructField("avatar_url", StringType(), True),
        StructField("url", StringType(), True),
        StructField("type", StringType(), True),
        StructField("site_admin", BooleanType(), True)
    ])
    
    data = [
        (101, "dev_test_1", "https://avatar.com/1", "https://github.com/1", "User", False),
        (102, "dev_test_2", "https://avatar.com/2", "https://github.com/2", "User", False)
    ]
    
    df_dummy = spark.createDataFrame(data, schema=schema)
    
    logger.info("Schema of Dummy DataFrame:")
    df_dummy.printSchema()
    df_dummy.show()
    
    logger.info("STEP 4: Writing to MongoDB via Spark...")
    writer = Spark_Write_Mongodb(spark, mongo_config)
    writer.spark_write_mongodb(df_dummy, collection_name="users", mode="append")
    
    logger.info("STEP 5: Testing Read back from MongoDB...")
    df_mongo = spark.read \
    .format("mongodb") \
    .option("database", mongo_config.database) \
    .option("collection", "users") \
    .load()
        
    df_mongo.show()
    logger.info("Test MongoDB pipeline SUCCESSFUL!")
    
    spark.stop()

if __name__ == "__main__":
    test_mongo_pipeline()