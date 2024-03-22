import psycopg2


class DBManager:
    """Класс для работы с базой данных"""

    @staticmethod
    def create_database(params, db_name):
        """Метод для создания новой базы данных."""
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name}")
        conn.close()

    @staticmethod
    def create_table_employees(cur):
        """Метод для создания таблицы с работодателями"""
        cur.execute("CREATE TABLE employees "
                    "(employee_id serial PRIMARY KEY, employee_name varchar(100) NOT NULL)")

    @staticmethod
    def create_table_vacancies(cur):
        """Метод для создания таблицы с вакансиями"""
        cur.execute("CREATE TABLE vacancies "
                    "(vacancy_id serial PRIMARY KEY, vacancy_name varchar(100) NOT NULL,"
                    "employee_id int REFERENCES employees(employee_id), min_pay int,"
                    "max_pay int, area varchar(100), http varchar(100) NOT NULL, title text)")

    @staticmethod
    def insert_to_table(vacancies_list, cur):
        """Метод для заполнения таблиц из списка экзепляров класса вакансий"""
        cur.execute(f"INSERT INTO employees (employee_name) VALUES ('{vacancies_list[0].employer}')")
        cur.execute(f"SELECT * FROM employees WHERE employee_name = '{vacancies_list[0].employer}'")
        employee_id = cur.fetchall()
        for vacancy in vacancies_list:
            cur.execute(
                "INSERT INTO vacancies (vacancy_name, employee_id, min_pay, max_pay, area, http, title)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (vacancy.name, employee_id[0][0], vacancy.min_pay, vacancy.max_pay, vacancy.area,
                 vacancy.url, vacancy.requirement))

    @staticmethod
    def get_companies_and_vacancies_count(cur):
        """Метод, получающий список всех компаний и количество вакансий у каждой компании"""
        cur.execute("SELECT employee_name, COUNT(*) FROM employees "
                    "JOIN vacancies USING (employee_id)"
                    "GROUP BY employee_name")
        companies_and_vacancies_count = cur.fetchall()
        return companies_and_vacancies_count

    @staticmethod
    def get_all_vacancies(cur):
        """Метод, получающий список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        cur.execute("SELECT employee_name, vacancy_name, min_pay, max_pay, http FROM vacancies "
                    "JOIN employees USING (employee_id)")
        all_vacancies = cur.fetchall()
        return all_vacancies

    @staticmethod
    def get_vacancies_with_keyword(keyword, cur):
        """Метод, получающий список всех вакансий, в названии которых содержатся переданные в метод слова"""
        list_keyword = keyword.split(' ')
        format_keyword = f"%{'%'.join(list_keyword)}%"
        cur.execute(f"SELECT * FROM vacancies WHERE vacancy_name LIKE '{format_keyword}'")
        vacancies_with_keyword = cur.fetchall()
        return vacancies_with_keyword

    @staticmethod
    def get_avg_salary(cur):
        """Метод, получающий среднюю зарплату по вакансиям (минимальную и максимальную)"""
        cur.execute("SELECT ROUND(AVG(min_pay)) as avg_min_pay, ROUND(AVG(max_pay)) as avg_max_pay "
                    "FROM vacancies")
        avg_salary = cur.fetchall()
        return (f"Средняя минимальная зарплата: {avg_salary[0][0]}\n"
                f"Средняя максимальная зарплата: {avg_salary[0][1]}")

    @staticmethod
    def get_vacancies_with_higher_salary(cur):
        """Метод, получает список всех вакансий, у которых зарплата (минимальная или максимальная) выше средней по всем вакансиям"""
        cur.execute("SELECT * FROM vacancies "
                    "WHERE min_pay > (SELECT ROUND(AVG(min_pay)) FROM vacancies) "
                    "OR max_pay > (SELECT ROUND(AVG(max_pay)) FROM vacancies)")
        vacancies_with_higher_salary = cur.fetchall()
        return vacancies_with_higher_salary
