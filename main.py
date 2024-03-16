from src.func import *

# создаем таблицы для работодателей и вакансий
employee = DBManager()
employee.create_table("employees", "employee_id serial PRIMARY KEY, employee_name varchar(100) NOT NULL")
vacancy = DBManager()
vacancy.create_table("vacancies", "vacancy_id serial PRIMARY KEY, vacancy_name varchar(100) NOT NULL,"
                                  "employee_id int REFERENCES employees(employee_id), min_pay int,"
                                  "max_pay int, area varchar(100), http varchar(100) NOT NULL, title text")

# заполняем таблицы вакансиями работодателей из списка
employers_list = ['ООО Открытый код', 'ООО МедиаСофт', 'Сбер для экспертов', 'ООО СимбирСофт',
                  'Inventale & Burt Intelligence', 'ООО Ростелеком Информационные Технологии', 'ИНТЕГРА-С', 'SberTech',
                  'Positive Technologies', 'АО Нэксайн']

insert_to_table(employers_list)
