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
        db.drop_collection("users")
        db.drop_collection("orgs")
        db.drop_collection("repos")
        db.drop_collection("events")

        logger2.info("Creating collections with strict JSON Schema Validation...")

     
        db.create_collection("users", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["_id", "login"], 
                "properties": {
                    "_id": {"bsonType": "int", "description": "user_id tu GitHub"},
                    "login": {
                        "bsonType": "string",
                        "maxLength": 65535
                    },
                    "avatar_url": {"bsonType": ["string", "null"], "maxLength": 65535},
                    "url": {"bsonType": ["string", "null"], "maxLength": 65535},
                    "type": {"bsonType": "string", "maxLength": 50, "enum": ["User", "Organization"]},
                    "site_admin": {"bsonType": "bool"}
                }
            }
        })

    
        db.create_collection("orgs", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["_id", "login"],
                "properties": {
                    "_id": {"bsonType": "int"},
                    "login": {"bsonType": "string", "maxLength": 255},
                    "url": {"bsonType": ["string", "null"], "maxLength": 65535}
                }
            }
        })

      
        db.create_collection("repos", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["_id", "full_name"],
                "properties": {
                    "_id": {"bsonType": "int"},
                    "name": {"bsonType": "string", "maxLength": 255},
                    "full_name": {"bsonType": "string", "maxLength": 255},
                    "url": {"bsonType": ["string", "null"], "maxLength": 65535},
                    "owner": {
                        "bsonType": "object",
                        "required": ["id"],
                        "properties": {
                            "id": {"bsonType": "int"}
                        }
                    }
                }
            }
        })

        db.create_collection("events", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["_id", "type", "actor", "repo"],
                "properties": {
                    "_id": {"bsonType": "long", "description": "Event ID tu GitHub API"},
                    "type": {"bsonType": "string", "maxLength": 50},
                    "actor": {
                        "bsonType": "object",
                        "required": ["id"],
                        "properties": {
                            "id": {"bsonType": "int"}
                        }
                    },
                    "repo": {
                        "bsonType": "object",
                        "required": ["id"],
                        "properties": {
                            "id": {"bsonType": "int"}
                        }
                    },
                    "created_at": {"bsonType": "string"}
                }
            }
        })

        logger2.info("Creating indexes for collection")
        db["users"].create_index([("login", 1)], unique=True)
        db["orgs"].create_index([("login", 1)], unique=True)
        db["repos"].create_index([("full_name", 1)], unique=True)
        db["repos"].create_index([("owner.id", 1)])
        db["events"].create_index([("actor.id", 1)])
        db["events"].create_index([("repo.id", 1)])
        logger2.info("Created MongoDB schema")
        return db
    
    except PyMongoError as e:
        logger2.error(f"Failed to create MongoDB schema: {str(e)}")
        raise e




        

