from celery import shared_task
import telebot
from django.conf import settings
from django.utils.timezone import now
from .models import Habit

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


@shared_task
def send_reminders():
    habits = Habit.objects.filter(next_reminder__lte=now(), is_public=False)
    for habit in habits:
        if habit.user.telegram_id:
            message = f"Напоминание о вашей привычке: {habit.name}"
            send_message(habit.user.telegram_id, message)

        habit.next_reminder += habit.reminder_interval
        habit.save()


def send_message(chat_id, text):
    bot.send_message(chat_id, text)
