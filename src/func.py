from src.api_services_classes import *
from src.DB_classes import *
from src.vacansy_class import *
from config import config


def add_employees():
    employees_list = []
    while True:
        employee = input("Введите название компании, для перехода к дальнейшим действиям введите 0: ")
        if employee == '0':
            break
        else:
            employees_list.append(employee)
    if len(employees_list) == 0:
        print("Вы не выбрали ни одной компании, до свидания.")
        exit()
    return employees_list


def insert_to_table(employers_list, cur):
    """Функция, заполняющая таблицы вакансиями работодателей из переданного списка"""
    hh_api = HeadHunterAPI()
    for employers in employers_list:
        hh_vacancies = hh_api.get_employer_vacancies(employers)
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
        DBManager.insert_to_table(vacancies_list, cur)


def user_interaction(parser, cur):
    while True:
        print(f"Выберите дальнейшее действие:\n"
              f"1 - Получить список всех компаний и количество их вакансий\n"
              f"2 - Получить список всех вакансий\n"
              f"3 - Получить список вакансий по ключевым словам\n"
              f"4 - Получить среднюю зарплату по вакансиям\n"
              f"5 - Получить вакансии с зарплатой выше средней\n"
              f"0 - Выход")
        user_answer = input("Ваш выбор: ")
        if user_answer == "1":
            for employee in parser.get_companies_and_vacancies_count(cur):
                print(employee)
        elif user_answer == "2":
            for vacancy in parser.get_all_vacancies(cur):
                print(vacancy)
        elif user_answer == "3":
            user_input = input("Введите ключевые слова через пробел: ")
            for vacancy in parser.get_vacancies_with_keyword(user_input, cur):
                print(vacancy)
        elif user_answer == "4":
            print(parser.get_avg_salary(cur))
        elif user_answer == "5":
            for vacancy in parser.get_vacancies_with_higher_salary(cur):
                print(vacancy)
        elif user_answer == "0":
            print("Спасибо, до новых встреч!")
            break
        else:
            print("Такой вариант отсутствует")


def main():
    params = config()
    conn = None
    db_name = "hh_parser"
    parser = DBManager()

    parser.create_database(params, db_name)
    params.update({'dbname': db_name})
    employers_list = add_employees()
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                parser.create_table_employees(cur)
                parser.create_table_vacancies(cur)
                insert_to_table(employers_list, cur)
                user_interaction(parser, cur)
    finally:
        if conn is not None:
            conn.close()
