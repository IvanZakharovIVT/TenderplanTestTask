from celery import Celery, Task

# Initialize Celery app
app = Celery('tasks', broker='redis://127.0.0.1:6379/0')

# Define subtasks
class SubTask1(Task):
    name = 'sub_task_1'

    def run(self, x, y):
        return x * y

class SubTask2(Task):
    name = 'sub_task_2'

    def run(self, x, y):
        return x ** y

# Define the parent task
class ParentTask(Task):
    name = 'parent_task'

    def run(self, x, y):
        # Execute subtask 1
        result1 = SubTask1().delay(x, y)

        # Execute subtask 2
        result2 = SubTask2().delay(x, y)

        # Wait for subtasks to complete and retrieve results
        result1_value = result1.get()
        result2_value = result2.get()

        # Perform some operation with subtask results
        return result1_value + result2_value

# Register tasks with the Celery app
app.tasks.register(SubTask1())
app.tasks.register(SubTask2())
app.tasks.register(ParentTask())

# Run the parent task asynchronously
result = ParentTask().delay(10, 2)

# Retrieve the result
print(result.get())