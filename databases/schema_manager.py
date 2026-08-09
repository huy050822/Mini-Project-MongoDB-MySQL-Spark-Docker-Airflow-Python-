#Database Schema Mongodb & Mysql
from config.logging_config import get_logger
from pymongo.errors import PyMongoError

logger1 = get_logger("mysql_schema_connect", "schema_manager.log")
logger2 = get_logger("mongodb_schema_connect", "schema_manager.log")


def create_mysql_schema(connection, cursor, dtb: str):
    
    cursor.execute(f"DROP DATABASE IF EXISTS {dtb}")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dtb}")
    logger1.info(f"Created database {dtb}")

    try:
        with open("E:\Mini Project 1\src\mysql\schema.sql", "r") as file:
            script = file.read()
            cursor.execute(f"USE {dtb}")
            #Eleminat space
            sql_command = [cmd.strip() for cmd in script.split(";") if cmd.strip()]

            for command in sql_command:
                cursor.execute(command) 
            connection.commit()
            logger1.info(f"Created MySQL schema")
            
    except ValueError as e:
        connection.rollback()
        logger1.error(f"Failed to create MySQL schema : {str(e)}")
        raise e
    
def create_mongodb_schema(client, db_name: str):

    try:
        db = client[db_name]
        logger2.info(f"Starting initialization for database: {db_name}")
        db.drop_collection("events")

        db.create_collection("events", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["id", "type"],  
                "properties": {
                    "type": {"bsonType": "string"}
                }
            }
        })

        # Tạo Index trên trường id gốc của GitHub để query/check trùng nhanh
        db["events"].create_index([("id", 1)])
        db["events"].create_index([("actor.id", 1)])
        db["events"].create_index([("repo.id", 1)])
     
    except PyMongoError as e:
        logger2.error(f"Failed to create MongoDB schema: {str(e)}")
        raise e




        

