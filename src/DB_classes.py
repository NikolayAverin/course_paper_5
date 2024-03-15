import psycopg2
from src.vacansy_class import *

class DBManager:
    """Класс для работы с базой данных"""
    @staticmethod
    def create_table(name, columns):
        """Метод для создания таблиц, передается название таблицы и колонки с описанием"""
        try:
            with psycopg2.connect(host='localhost', database='course_paper_5', user='postgres', password='111111') as conn:
                with conn.cursor() as cur:
                    cur.execute(f"CREATE TABLE {name} ({columns})")
        finally:
            conn.close()

    @staticmethod
    def insert_to_table(vacancies_list):
        """Метод для заполнения таблиц из списка экзепляров класса вакансий"""
        try:
            with psycopg2.connect(host='localhost', database='course_paper_5', user='postgres', password='111111') as conn:
                with conn.cursor() as cur:
                    cur.execute(f"INSERT INTO employees (name) VALUES ('{vacancies_list[0].employer}')")
                    cur.execute("SELECT * FROM employees WHERE name = 'emp3'")
                    employee_id = cur.fetchall()
                    for vacancy in vacancies_list:
                        cur.execute(
                            "INSERT INTO vacancies (name, employee_id, min_salary, max_salary, area, http, title)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (vacancies_list[0].name, employee_id[0][0], vacancies_list[0].min_pay,
                             vacancies_list[0].max_pay, vacancies_list[0].area, vacancies_list[0].url,
                             vacancies_list[0].requirement))
        finally:
            conn.close()