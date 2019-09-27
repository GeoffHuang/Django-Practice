from celery.decorators import task
from celery.utils.log import get_task_logger

from .emails import send_email
from .models import Question

logger = get_task_logger(__name__)


@task(name="send_email_task")
def send_email_task(message):
    """sends an email when a new poll is created"""
    logger.info("Sent new poll emails")
    return send_email(message)


@task(name="change_poll_status_task")
def change_poll_status_task(question_text):
    """changes the status of a new poll from 'processing' to 'ready'"""
    q = Question.objects.get(question_text=question_text)
    q.status = "ready"
    q.save()
    logger.info("Changed poll status")
    return
