from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    update.message.reply_text('Привет! Я ваш менеджер задач. Используйте команды для работы с задачами.')

def add_topic(update, context):
    topic_name = ' '.join(context.args)
    task_manager.add_topic(topic_name)
    update.message.reply_text(f'Тема "{topic_name}" добавлена.')

def add_task(update, context):
    task_text, topic_name = ' '.join(context.args).split('|')
    task_manager.add_task(task_text.strip(), topic_name.strip())
    update.message.reply_text(f'Задача "{task_text.strip()}" для темы "{topic_name.strip()}" добавлена.')

def get_tasks(update, context):
    topic
