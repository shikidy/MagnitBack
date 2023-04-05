import os
import time
import psycopg2
import psycopg2.extras

import secret


class DbWorker():

    # Создание подключения к базе данных
    # 
    def __init__(self, db_name) -> None:
        self.connection = psycopg2.connect(
            host=secret.DB_HOST,
            database=db_name,
            user=secret.DB_USER,
            password=secret.DB_PASSWORD
        )
        self.cache = {}
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Декоратор для кеширования запросов
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
    
    # Получение всех проектов
    @cache_analyse
    def get_projects(self):
        with self.connection:
            self.cursor.execute('SELECT * FROM projects')
            return self.cursor.fetchall()
        
    # Получение всех пользователей
    def get_user_by_log_pas(self, login: str, password: str):
        with self.connection:
            self.cursor.execute('SELECT * FROM users WHERE username = %s AND pass = %s', (login, password))
            return self.cursor.fetchone()
        
    # Получение всех территорий по id проекта
    def get_areas_by_project(self, project_id: int):
        with self.connection:
            self.cursor.execute('SELECT * FROM areas WHERE project_id = %s', (project_id,))
            return self.cursor.fetchall()

    # Получение всех линий по id территории
    def get_lines_by_area(self, area_id: int):
        with self.connection:
            self.cursor.execute('SELECT * FROM lines WHERE area_id = %s', (area_id,))
            return self.cursor.fetchall()

    # Получение всех точек по id линии
    def get_points_by_line(self, line_id: int):
        with self.connection:
            self.cursor.execute('SELECT * FROM points WHERE line_id = %s', (line_id,))
            return self.cursor.fetchall()
        
    # Получение всех результатов по id точки 
    def result_by_point(self, point_id: int):
        with self.connection:
            self.cursor.execute('SELECT * FROM point_result WHERE point_id = %s', (point_id,))
            return self.cursor.fetchall()
        
    # Создание проекта
    def create_project(self, user_id: int, name: str):
        with self.connection:
            self.cursor.execute("SELECT id FROM projects ORDER BY id DESC limit 1")
            data = self.cursor.fetchone()['id'] + 1

            self.cursor.execute("INSERT INTO projects (id, creator_id, name) VALUES (%s, %s, %s)", (data, user_id, name))
    
    # Удаление проекта
    def delete_project(self, id: int):
        with self.connection:
            self.cursor.execute("DELETE FROM projects WHERE id = %s", (id, ))

    # Создание территории
    def create_area(self, project_id: int, name: str):
        with self.connection:
            self.cursor.execute("SELECT id FROM areas ORDER BY id DESC limit 1")
            data = self.cursor.fetchone()['id'] + 1
            self.cursor.execute("INSERT INTO areas (id, project_id, name) VALUES (%s, %s, %s)", (data, project_id, name))

    # Удаление территории
    def delete_area(self, id: int):
        with self.connection:
            self.cursor.execute("DELETE FROM areas WHERE id = %s", (id,))   
            
    def get_all_points_by_area(self, line_id: int):
        with self.connection:
            self.cursor.execute("SELECT DISTINCT  points.id, points.line_id, points.x, points.y, (SELECT AVG(T_data) from point_result WHERE point_result.point_id = points.id) as t FROM points,  lines, areas, point_result WHERE  %s = lines.area_id and lines.id =  points.line_id", (line_id,))
            return self.cursor.fetchall()
        
if __name__ == '__main__':
    a = DbWorker()
    print(a.get_areas_by_project(0))
