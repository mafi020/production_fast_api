from app.core.celery_app import celery_app
import time

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def send_email(self, email: str):
    time.sleep(5)  # simulate heavy work
    print(f"Email sent to {email}")
    return {"status": "sent"}
