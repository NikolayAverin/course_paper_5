from src.DB_classes import *

# создаем таблицы для работодателей и вакансий
employee = DBManager()
employee.create_table("employees", "employee_id serial PRIMARY KEY, name varchar(100) NOT NULL")
vacancy = DBManager()
vacancy.create_table("vacancies", "vacancy_id serial PRIMARY KEY, name varchar(100) NOT NULL,"
                                  "employee_id int REFERENCES employees(employee_id), min_salary int,"
                                  "max_salary int, area varchar(100), http varchar(100) NOT NULL, title text")

# получаем вакансии всех работодателей из списка и заполняем таблицы
employers_list = ['ООО Открытый код']