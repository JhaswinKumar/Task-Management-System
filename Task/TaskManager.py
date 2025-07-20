from Enums import TaskStatus as taskstatus
from Enums import TaskPriority as taskpriority
import DataBase.Manager.DatabaseManager as dbManager
import Task.Task as tsk

from  datetime import datetime


import threading

class TaskManager:
    def __init__(self):
       self.db = dbManager.DatabaseManager()
       self.lock =threading.Lock()


    def create_task(self, title : str,description : str, assigned_to : str, priority : taskpriority.TaskPriority ,due_date : str):

        with self.lock:
            cursor = self.db.conn.cursor()
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


    def get_all_tasks(self):
        cursor =  self.db.conn.cursor()
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

    def update_task_status(self,task_id : int,new_status : taskstatus.TaskStatus):
          
          with self.lock:
            cursor =  self.db.conn.cursor()
            completed_at =None

            if new_status == taskstatus.TaskStatus.COMPLETED.value:
                completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute('''UPDATE  tasks SET status =%s, completed_at =%s WHERE task_id =%s
                          ''', (new_status,completed_at,task_id))    
            
            self.db.conn.commit()
            return cursor.rowcount >0
    

    def add_commant(self,task_id :int, comment:str):
        with self.lock:
            cursor =  self.db.conn.cursor()
            cursor.execute('''
                    INSERT INTO comments (task_id,comment, timestamp) VALUES(%s,%s,%s)
                           ''',(task_id,comment,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
            self.db.conn.commit()
            return True

    def get_task_comments(self, task_id :int):
        
        cursor =self.db.conn.cursor()
        cursor.execute('SELECT comment, timestamp FROM comments WHERE task_id = %s',(task_id,))
        return cursor.fetchall()

