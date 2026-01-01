import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

#Get logger
logger = logging.getLogger(__name__)

#Set up MongoDB
class MongoDB_connect():
    def __init__(self, mongo_uri, database):
        self.mongo_uri = mongo_uri
        self.database = database
        self.client = None
        self.db = None

    def __repr__(self):
        return f"MongoDB(mongo_uri{self.mongo_uri}, database{self.database})"
    
    def connector(self):
        try:
            logger.info("Connecting to MongoDB")
            #Connect
            self.client = MongoClient(self.mongo_uri)

            #Test connection
            self.client.admin.command("ping")
            self.db = self.client[self.database]
            logger.info(f"MongoDB was connected successfully to database: {self.database}")
        
        except Exception as e:
            logger.error("Fail to connect MongoDB", exc_info=True)
            raise RuntimeError("MongoDB connection failed") from e

    
    def close(self):
        try:
            if self.client:
                self.client.close()
            
            logger.info("Closed MongoDB")
        except Exception:
            logger.error("Fail to close", exc_info=True)

    def __enter__(self):
        return self  

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()