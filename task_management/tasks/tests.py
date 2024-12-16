# tasks/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task

@shared_task
def send_task_reminder():
    # Find tasks due in next 24 hours
    tasks = Task.objects.filter(
        due_date__lte=timezone.now() + timezone.timedelta(hours=24),
        status__in=['pending', 'in_progress']
    )

    for task in tasks:
        send_mail(
            'Task Reminder',
            f'Reminder: Your task "{task.title}" is due soon.',
            'noreply@yourdomain.com',
            [task.user.email],
            fail_silently=False,
        )