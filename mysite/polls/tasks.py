from celery.decorators import task
from celery.utils.log import get_task_logger

from .emails import send_feedback_email

logger = get_task_logger(__name__)


@task(name="send_feedback_email_task")
def send_feedback_email_task(message):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent new poll emails")
    return send_feedback_email(message)
