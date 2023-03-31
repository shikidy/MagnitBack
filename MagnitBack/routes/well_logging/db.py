import os
import time
import psycopg2
import psycopg2.extras

import secret


class DbWorker():

    def __init__(self, db_name) -> None:
        self.connection = psycopg2.connect(
            host=secret.DB_HOST,
            database=db_name,
            user=secret.DB_USER,
            password=secret.DB_PASSWORD
        )
        self.cache = {}
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def cache_analyse(func):

        def wrapper(self, *arg, **kwargs):
            func_name = str(func)
            if not func_name in self.cache:
                self.cache[func_name] = {
                    'data' : '',
                    'time' : 0
                }
            if int(time.time()) -  self.cache[func_name]['time'] < 0.5:
                print('returned cache')
                return self.cache[func_name]['data']
            try:
                data = func(self, *arg, **kwargs)
            except:
                if self.cache[func_name]['data']:
                    return self.cache[func_name]['data']
                raise Exception('Err on get response from db')
            self.cache[func_name] = {
                'data' : data,
                'time' : int(time.time())
            }
            return data
        return wrapper


    def get_projects_by_user(self, user_id: int):
        with self.connection:
            self.cursor.execute('SELECT * FROM Projects WHERE user_id = %s', (user_id,))
            return self.cursor.fetchall()
        
    def get_user_by_log_pas(self, login: str, password: str):
        with self.connection:
            self.cursor.execute('SELECT * FROM users WHERE full_name = %s AND pass = %s', (login, password))
            return self.cursor.fetchone()
        
    def get_pickets_by_area(self, area_id: int):
        with self.connection:
            self.cursor.execute('SELECT * FROM pickets WHERE area_id = %s', (area_id,))
            return self.cursor.fetchall()
        
    def get_areas_by_project(self, project_id: int):
        with self.connection:
            self.cursor.execute('SELECT * FROM areas WHERE project_id = %s', (project_id,))
            return self.cursor.fetchall()


        
if __name__ == '__main__':
    a = DbWorker()
    print(a.get_areas_by_project(0))
