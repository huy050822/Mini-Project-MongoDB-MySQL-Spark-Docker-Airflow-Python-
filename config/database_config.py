# Get thông tin database từ file .env 
import os
from dotenv import load_dotenv
from dataclasses import dataclass

#Config MySql

# host = os.getenv("MYSQL_HOST")
# port = os.getenv("MYSQL_PORT")
# user = os.getenv("MYSQL_USER")
# password = os.getenv("MYSQL_PASSWORD")
# database = os.getenv("MYSQL_DATABASE")
# print(host,port,user,database,password)

#configuration object 
@dataclass
class Mysql_Config():
    host : str
    port : int
    user : str
    password : str
    database : str

@dataclass
class Mongodb_Config():
    uri : str
    database : str

def get_database_config():
    # read data from .env file
    load_dotenv()

    config = {
        "mysql" : Mysql_Config(
            host = os.getenv("MYSQL_HOST"),
            port = os.getenv("MYSQL_PORT"),
            user = os.getenv("MYSQL_USER"),
            password = os.getenv("MYSQL_PASSWORD"),
            database = os.getenv("MYSQL_DATABASE")
        ),
        "mongodb" : Mongodb_Config(
            uri = os.getenv("MONGODB_URI"),
            database = os.getenv("MONGODB_DATABASE")
        )
    }

    return config
