from enum import Enum

class TaskStatus(Enum):
    TODO="To Do"
    IN_PROGRESS ="In Progress"
    COMPLETED ="Completed"
    BLOCKED ="Blocked"
