from Enums import TaskStatus as taskstatus
from Enums import TaskPriority as taskpriority
import DataBase.Manager.DatabaseManager as dbManager
import Task.Task as tsk
from Logger.LoggerManager import LoggerManager

from  datetime import datetime
import threading

class TaskManager:
    def __init__(self):
       self.logger = LoggerManager.get_logger("TaskManager")
       self.db = dbManager.DatabaseManager()
       self.lock =threading.Lock()

    def create_task(self, title : str,description : str, assigned_to : str, priority : taskpriority.TaskPriority ,due_date : str):
        with self.lock:
            cursor = self.db.conn.cursor()
            try:
                 cursor.execute('''
                        INSERT INTO tasks (title, description, assigned_to, priority, status, due_date, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING task_id
                    ''', (
                        title,
                        description,
                        assigned_to,
                        priority,
                        taskstatus.TaskStatus.TODO.value,
                        due_date,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ))
                 task_id = cursor.fetchone()[0]
                 self.db.conn.commit()          
                 return task_id
            except Exception as ex:
                self.db.conn.rollback()
                self.logger.error(f"Failed to create task: {ex}")
            finally:
                cursor.close()


    def get_all_tasks(self):
        cursor =  self.db.conn.cursor()
        try:
            cursor.execute('SELECT *FROM tasks')
            tasks = []
            for row in cursor.fetchall():
                task = tsk.Task(
                    task_id = row[0],
                    title=row[1],
                    description=row[2],
                    assigned_to=row[3],
                    priority= row[4],
                    status=row[5],
                    due_date=row[6],
                    created_at=row[7],
                    completed_at= row[8]
                )
                tasks.append(task)
            return tasks  
        except Exception as ex:
             self.db.conn.rollback()
             self.logger.error(f"Failed to read tasks: {ex}")
             return tasks
        finally:
            cursor.close()  

    def update_task_status(self,task_id : int,new_status : taskstatus.TaskStatus):          
          with self.lock:
            cursor =  self.db.conn.cursor()
            completed_at =None
            try:
                if new_status == taskstatus.TaskStatus.COMPLETED.value:
                    completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute('''UPDATE  tasks SET status =%s, completed_at =%s WHERE task_id =%s
                               ''', (new_status,completed_at,task_id))  
                
                self.db.conn.commit()
                return cursor.rowcount >0
            except Exception as ex:
                self.db.conn.rollback()
                self.logger.error(f"Failed to update task status: {ex}")
                return 0
            finally:
                cursor.close()
               
            
    

    def add_commant(self,task_id :int, comment:str):
        with self.lock:
            cursor =  self.db.conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO comments (task_id,comment, timestamp) VALUES(%s,%s,%s)
                           ''',(task_id,comment,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
                self.db.conn.commit()
                return True
            except Exception as ex:
                self.db.conn.rollback()
                self.logger.error(f"Failed to update task status: {ex}")
                return False
            finally:
                cursor.close()

    def get_task_comments(self, task_id :int):        
        cursor =self.db.conn.cursor()
        try:
            cursor.execute('SELECT comment, timestamp FROM comments WHERE task_id = %s',(task_id,))
            return cursor.fetchall()
        except Exception as ex:
             self.logger.error(f"Failed to get task comments: {ex}")
             return None
        finally:
            cursor.close()


