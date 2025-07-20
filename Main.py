
import Task.TaskManager as taskmanager
import Reports.TaskAnalytics as taskAnalytics
from Enums import TaskPriority as taskpriority
from Enums import TaskStatus as taskstatus
from Logger.LoggerManager import LoggerManager


def main():
   task_manager = taskmanager.TaskManager()
   analytics = taskAnalytics.TaskAnylytics(task_manager)
   logger =LoggerManager.get_logger("Main")

   def print_menu():
       print("\n=== Task Management System ===")
       print("1.  Create New Task")
       print("2.  List All Tasks")
       print("3.  Update Task Status")
       print("4.  Add Comment to Task")
       print("5.  Generate Analytics")
       print("6.  View Task Summary")
       print("7.  Exit")
       print("========================================")

   def create_task():
       try:
           print("\nCreate New Task:")

           title = input("Enter task title: ")
           description = input("Enter task description: ")
           assigned_to = input("Assin to: ")
           print("\nPriority Levels:", [p.value for p in taskpriority.TaskPriority])
           priority = input("Enter priority: ")
           due_date = input("Enter due date (YYYY-MM-DD): ")

           task_id =task_manager.create_task(title,
                                             description,
                                             assigned_to,
                                             priority,
                                             due_date)
           print(f"\nTask created successfully with ID : {task_id}")
           logger.info(f"Task created successfully with ID : {task_id}")
       except Exception as ex:
           logger.error(f"Create task function failure {ex}")
       

   def list_tasks():
       print("\nAll Tasks:")
       print("-"*85)
       tasks =task_manager.get_all_tasks()

       for task in tasks:
           print(f"\nTask ID: {task.task_id}")
           print(f"\nTitle: {task.title}")
           print(f"\nAssigned to: {task.assigned_to}")
           print(f"\nStatus: {task.status}")
           print(f"\nPriority: {task.priority}")
           print(f"\nTDue Date: {task.due_date}")

           comments = task_manager.get_task_comments(task.task_id)
           if comments:
               print("Comments:")
               for comment,timestamp in comments:
                   print(f"- {comment} ({timestamp})")

           print("-"*85)   

   def update_status():
       task_id =int(input("\nEnter Task ID: "))
       print("Available statuses:",[s.value for s in taskstatus.TaskStatus])    
       new_status = input("Enter new status: ")

       if task_manager.update_task_status(task_id,new_status):
           print("Status updated successfully")
       else:
           print("Task not found")        

   def add_comment():
       task_id = int(input("\nEnter Task ID: "))
       comment = input("Enter commnet: ")

       if task_manager.add_commant(task_id,comment):
           print("Comment added successfully")
       else:
           print("Task not found")

   def generate_analytics():
       analytics.plot_task_statistics()
       print("\nAnalytics charts have been saved as 'task_analytics.png'")
   
   def view_summary():
       summmary =analytics.generate_summary_report()
       print("\nTask Summary:")

       print("-"*30)
       for key,value in summmary.items():
           print(f" {key}: {value}")


   while True:
       print_menu()

       try:
           choice = int(input("Enter your choice (1-7): ")) 
           if choice == 1:
               create_task()
           elif choice == 2:
               list_tasks()
           elif choice == 3:
               update_status()
           elif choice == 4:
               add_comment()
           elif choice == 5:
               generate_analytics()
           elif choice == 6:
               view_summary()
           elif choice == 7:
               print("Exiting... Goodbye!")
               break
           else:
               print("Invalid choice. Please enter a number between 1 and 7.")
       except ValueError:
           print("Invalid input. Please enter a valid number.")



if __name__=="__main__":
    main()

