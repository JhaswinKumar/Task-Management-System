from Enums import TaskStatus as taskstatus
from Enums import TaskPriority as taskpriority
from  datetime import datetime,timedelta

class Task:
    def __init__(self,task_id,title,description, assigned_to,priority,due_date,status = taskstatus.TaskStatus.TODO.value, created_at = None,completed_at =None):
        self.task_id =task_id
        self.title =title
        self.description =description
        self.assigned_to=assigned_to
        self.priority = priority
        self.due_date =due_date
        self.status =status
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_at = completed_at