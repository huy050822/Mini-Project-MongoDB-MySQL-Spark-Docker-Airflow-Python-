import logging

#Get logger
logger = logging.getLogger(__name__)

#Set up MongoDB
class MongoDB_connect():
    def __init__(self, mongo_uri, database):
        self.mongo_uri = mongo_uri
        self.database = database
    
    def __repr__(self):
        return f"MongoDB(mongo_uri{self.mongo_uri}, database{self.database})"
    
    def mongodb_connector(self):
        try:
            logger.info("Connecting to MongoDB")
        

        except Exception:
            logger.error("Fail to connect MongoDB", exc_info=True)
            return None, None