from celery import Celery, Task

# Initialize Celery
app = Celery('tasks', broker='redis://localhost:6379/0')
app.conf.broker_url = 'redis://localhost:6379/0'

# app.start()


# Define a simple task
@app.task
def add(x, y):
    print("я нихуя не понял")
    return x + y


class EmailTask(Task):
    name = "email_task"

    def run(self, link_url: str, count: int):
        print(link_url, count)
        try:
            t = link_url * count
            return t
        except Exception:
            return 123


app.register_task(EmailTask())

# Calling the task
result = add.delay(4, 5)
result2 = EmailTask().delay('br', 5)
# print(result.get())

