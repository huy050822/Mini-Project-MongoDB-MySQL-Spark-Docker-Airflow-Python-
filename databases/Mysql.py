import mysql
import _mysql_connector

class MySQL_connect:
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

    def __repr__(self):
        return f"MySQL(host{self.host},port{self.port},user{self.user},database{self.database})"
    

    def connector(self):
        self.connection = mysql.connector.connect(**self.config)

def main():
    print()

if __name__ == "__main__":
    main()