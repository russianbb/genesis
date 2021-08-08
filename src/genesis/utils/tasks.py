from celery_app import app


@app.task(bind=True)
def task_ping(self):
    print(f"PONG: {self.request!r}")  # noqa: T001
