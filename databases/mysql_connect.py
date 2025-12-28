import mysql.connector
import logging


#Get logger 
logger = logging.getLogger(__name__)

# Set up MYSQL connect
class MySQLConnect:
    #Init Function
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user 
        self.password = password
        self.database = database
        self.config = {
            "host" : host,
            "port" : port,
            "user" : user,
            "password" : password,
            "database" : database            
       }
        self.connection = None
        self.cursor = None  
    #Repr Function
    def __repr__(self):
        return f"MySQL(host{self.host},port{self.port},user{self.user},database{self.database})"
    
    #Connect to MySQL
    def connector(self):
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()
        return self.connection, self.cursor
    
    def close(self):
        try:
            #Close cursor
            if self.cursor:
                self.cursor.close()
            
            #Close connection
            if self.connection and self.connection.is_connected():
                self.connection.close()

            logger.info("Closed MySQL")

        except Exception:
            #Show logging (error)
            logger.error("Fail to close", exc_info= True)
        
    def __enter__(self):
        try:
            logger.info("Connecting to MySQL")
            self.connector()
            logger.info("MySQL was connected successfully")
            return self
        except Exception:
            #Show logging (error)
            logger.error("Fail to connect MySQL", exc_info= True)
            


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


