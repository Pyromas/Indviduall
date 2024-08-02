import sqlite3
from datetime import datetime

class TaskManager:
    def __init__(self, db_name='task_manager.db'):
        self.db_name = db_name

    def _execute_query(self, query, params=()):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        result = cursor.fetchall()
        conn.close()
        return result

    def add_topic(self, topic_name):
        self._execute_query('INSERT INTO topics (name) VALUES (?)', (topic_name,))

    def add_task(self, task_text, topic_name):
        topic_id = self._execute_query('SELECT id FROM topics WHERE name = ?', (topic_name,))
        if topic_id:
            self._execute_query('INSERT INTO tasks (task, topic_id) VALUES (?, ?)', (task_text, topic_id[0][0]))
        else:
            self._execute_query('INSERT INTO tasks (task) VALUES (?)', (task_text,))

    def get_tasks_by_topic(self, topic_name):
        return self._execute_query('''
            SELECT tasks.id, tasks.task, tasks.created_at, tasks.updated_at, tasks.status
            FROM tasks
            JOIN topics ON tasks.topic_id = topics.id
            WHERE topics.name = ?
        ''', (topic_name,))

    def get_all_tasks(self):
        return self._execute_query('''
            SELECT tasks.id, tasks.task, topics.name, tasks.created_at, tasks.updated_at, tasks.status
            FROM tasks
            LEFT JOIN topics ON tasks.topic_id = topics.id
        ''')

    def get_all_topics(self):
        return self._execute_query('SELECT * FROM topics')

    def update_task(self, task_id, new_task_text=None, new_topic_name=None, status=None):
        updates = []
        params = []

        if new_task_text:
            updates.append('task = ?')
            params.append(new_task_text)
        
        if status:
            updates.append('status = ?')
            params.append(status)
        
        if new_topic_name:
            new_topic_id = self._execute_query('SELECT id FROM topics WHERE name = ?', (new_topic_name,))
            if new_topic_id:
                updates.append('topic_id = ?')
                params.append(new_topic_id[0][0])

        updates.append('updated_at = ?')
        params.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        params.append(task_id)

        self._execute_query(f'UPDATE tasks SET {", ".join(updates)} WHERE id = ?', params)

    def delete_task(self, task_id):
        self._execute_query('DELETE FROM tasks WHERE id = ?', (task_id,))

    def delete_topic(self, topic_name):
        topic_id = self._execute_query('SELECT id FROM topics WHERE name = ?', (topic_name,))
        if topic_id:
            self._execute_query('DELETE FROM tasks WHERE topic_id = ?', (topic_id[0][0],))
            self._execute_query('DELETE FROM topics WHERE id = ?', (topic_id[0][0],))


task_manager = TaskManager()


task_manager.add_topic('Работа')
task_manager.add_topic('Личное')


task_manager.add_task('Закончить отчет', 'Работа')
task_manager.add_task('Купить продукты', 'Личное')


tasks = task_manager.get_tasks_by_topic('Работа')
for task in tasks:
    print(f'ID: {task[0]}, Task: {task[1]}, Created: {task[2]}, Updated: {task[3]}, Status: {task[4]}')


task_manager.update_task(1, new_task_text='Закончить отчет до конца недели', status='выполнена')


task_manager.delete_task(2)


task_manager.delete_topic('Личное')
