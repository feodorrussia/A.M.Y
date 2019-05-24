import sqlite3


class Session:
    def __init__(self):
        if 'data' not in __import__('os').listdir('.'):
            __import__('os').mkdir('data')
        self.connection = sqlite3.connect("data/alisa_sessions.db", isolation_level=None)
        cursor = self.connection.cursor()
        cursor.execute('PRAGMA foreign_key=1')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sessions
                            (user_id TEXT,
                            user_name VARCHAR(80),
                            recipient_name VARCHAR(80),
                            status_action VARCHAR(50))''')
        cursor.close()

    def __del__(self):
        self.connection.close()

    def add_session(self, user_id):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                '''INSERT INTO sessions  VALUES(:user_id, :user_name, :recipient_name, :status_action)''',
                {'user_id': ''.join([str(x) for x in user_id]), 'user_name': "", 'recipient_name': "", 'status_action': "login"})
        except sqlite3.DatabaseError as error:
            print('Error: ', error, '1')
            cursor.close()
            return False
        else:
            cursor.close()
            return True

    def update_status_system(self, new, user_id, group='status_action'):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""UPDATE sessions
                            SET {group} = ?
                            WHERE user_id = ? """, (new, user_id))
        except sqlite3.DatabaseError as error:
            print('       !!!!!!!!!!!!!!!!!Error: ', error)
            cursor.close()
            return False
        else:
            cursor.close()
            return True

    def get_session(self, user_id='', group='*', all=False) -> list:
        cursor = self.connection.cursor()
        try:
            if all:
                cursor.execute("""SELECT user_id FROM sessions""")
                session = [x[0] for x in cursor.fetchall()]
            else:
                cursor.execute(
                    f"""SELECT {group} FROM sessions WHERE user_id = :user_id""",
                    {'user_id': user_id})
                session = cursor.fetchall()[0]
        except sqlite3.DatabaseError as error:
            print('Error: ', error, '2')
            cursor.close()
            return [False]
        else:
            cursor.close()
            return session