from Logger.LoggerManager import LoggerManager

import psycopg2
import threading
from dotenv import load_dotenv
import os


 
class DatabaseManager:
    def __init__(self):
        self.logger = LoggerManager.get_logger("DatabaseManager")
        self.conn= self.get_db_connection()
        self.lock = threading.Lock()
        self.create_tables()


    def get_db_connection(self):
        try:

           if load_dotenv('DataBase\.env'):
                 USER = os.getenv('user')
                 PASSWORD = os.getenv('password')
                 HOST = os.getenv('host')
                 PORT = os.getenv('port')
                 DB_NAME = os.getenv('dbname')

           return  self.connect_to_postgres(DB_NAME, USER, PASSWORD, HOST, PORT)
        
        except Exception as ex:
            print(f"Error occured while creating connection to DB {DB_NAME}, Error : {ex}")
            self.logger.error(f"Create task function failure {ex}")
            return None
    
    def connect_to_postgres(self,db_name, user, password, host, port):        
        connection = None
        try:
            connection = psycopg2.connect(
                database=db_name,
                user=user,
                password=password,
                host=host,
                port=port,
            )
            print(f"Connection to postgresSQL DB({db_name}) Successful")
            self.logger.info(f"Connection to postgresSQL DB({db_name}) Successful")
            return connection
        except Exception as e:
            print(f"Error occured while creating connection to DB {db_name}, Error : {e}")
            self.logger.error(f"Error occured while creating connection to DB {db_name}, Error : {e}")
            return connection

    def create_tables(self):
        with self.lock:
            cursor = self.conn.cursor()
            try:
                #Tasks table
                cursor.execute('''
                               CREATE TABLE IF NOT EXISTS tasks(
                                task_id SERIAL PRIMARY KEY,
                                title TEXT NOT NULL,
                                description TEXT,
                                assigned_to TEXT,
                                priority TEXT,
                                status TEXT,
                                due_date TEXT,
                                created_at TEXT,
                                completed_at TEXT
                            )''')
            

                #Comments table
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS comments (
                            comment_id SERIAL PRIMARY KEY,
                            task_id INTEGER REFERENCES tasks(task_id),
                            comment TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                        ''')
            
                self.conn.commit()

            except Exception as ex:
                self.logger.error(f"Error occured while creating tables into DB, Error : {ex}")     

            finally:
                cursor.close()
