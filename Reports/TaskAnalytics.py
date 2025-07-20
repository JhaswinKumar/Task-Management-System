#import Task.TaskManager as taskmanager

from Enums import TaskStatus as taskstatus
from Enums import TaskPriority as taskpriority


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class TaskAnylytics:
    def __init__(self,task_manager):
        self.task_manager = task_manager

    def get_tasks_dataframe(self):
        tasks = self.task_manager.get_all_tasks()
        data =[]
        for task in tasks:
            data.append({
                'task_id' : task.task_id,
                'title':task.title,
                'status': task.status,
                'priority': task.priority,
                'assigned_to' : task.assigned_to,
                'due_date':task.due_date,
                'created_at': task.created_at,
                'completed_at': task.completed_at
            })

        return data    

    def plot_task_statistics(self):

        df = pd.DataFrame(self.get_tasks_dataframe())

        fig =plt.figure(figsize=(12,8))

        #1. Status Distribution
        plt.subplot(2,2,1)
        status_count =df['status'].value_counts()
        sns.barplot(x= status_count.index,y=status_count.values)
        plt.title('Task Status Distribution')
        plt.xticks(rotation =45)


        #2. Priority Distribution

        plt.subplot(2,2,2)
        priority_counts = df['priority'].value_counts()
        sns.barplot(x= priority_counts.index,y=priority_counts.values)
        plt.title('Task Priority Distribution')
        plt.xticks(rotation =45)


        #3. User WorkLoad

        plt.subplot(2,2,3)
        user_counts = df[df['status'] != taskstatus.TaskStatus.COMPLETED.value]['assigned_to'].value_counts()
        sns.barplot(x= user_counts.index,y=user_counts.values)
        plt.title('Active Task per user')
        plt.xticks(rotation =45)


        #4. Tasks Timeline

        plt.subplot(2,2,4)
        df['created_at'] = pd.to_datetime(df['created_at'])
        tasks_per_day =df.groupby(df['created_at'].dt.date).size()
        sns.lineplot(x=tasks_per_day.index, y= tasks_per_day.values)
        plt.title('Tasks created Over Time')
        plt.xticks(rotation =45)

        plt.tight_layout()
        plt.savefig('task_analytics.png')
        plt.show()

    def generate_summary_report(self):

        df = pd.DataFrame(self.get_tasks_dataframe())

        summary ={

            'Total Tasks': len(df),
            'Completed Tasks' : len(df[df['status'] == taskstatus.TaskStatus.COMPLETED.value]),
            'Pending Tasks': len(df[df['status'] != taskstatus.TaskStatus.COMPLETED.value]),
            'High Priority Tasks': len(df[df['priority'] == taskpriority.TaskPriority.HIGH.value]),
            'Critical Tasks' : len(df[df['priority'] == taskpriority.TaskPriority.CRITICAL.value]),
        }
        return summary




    
