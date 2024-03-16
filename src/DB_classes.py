import psycopg2


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
                    cur.execute(f"INSERT INTO employees (employee_name) VALUES ('{vacancies_list[0].employer}')")
                    cur.execute(f"SELECT * FROM employees WHERE employee_name = '{vacancies_list[0].employer}'")
                    employee_id = cur.fetchall()
                    for vacancy in vacancies_list:
                        cur.execute(
                            "INSERT INTO vacancies (vacancy_name, employee_id, min_pay, max_pay, area, http, title)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (vacancy.name, employee_id[0][0], vacancy.min_pay, vacancy.max_pay, vacancy.area,
                             vacancy.url, vacancy.requirement))
        finally:
            conn.close()

    @staticmethod
    def get_companies_and_vacancies_count():
        """Метод, получающий список всех компаний и количество вакансий у каждой компании"""
        try:
            with psycopg2.connect(host='localhost', database='course_paper_5', user='postgres', password='111111') as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT employee_name, COUNT(*) FROM employees "
                                "JOIN vacancies USING (employee_id)"
                                "GROUP BY employee_name")
                    companies_and_vacancies_count = cur.fetchall()
        finally:
            conn.close()
            return companies_and_vacancies_count

    @staticmethod
    def get_all_vacancies():
        """Метод, получающий список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        try:
            with psycopg2.connect(host='localhost', database='course_paper_5', user='postgres', password='111111') as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT employee_name, vacancy_name, min_pay, max_pay, http FROM vacancies "
                                "JOIN employees USING (employee_id)")
                    all_vacancies = cur.fetchall()
        finally:
            conn.close()
            return all_vacancies

    @staticmethod
    def get_vacancies_with_keyword(keyword):
        """Метод, получающий список всех вакансий, в названии которых содержатся переданные в метод слова"""
        list_keyword = keyword.split(' ')
        format_keyword = f"%{'%'.join(list_keyword)}%"
        try:
            with psycopg2.connect(host='localhost', database='course_paper_5', user='postgres', password='111111') as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT * FROM vacancies WHERE vacancy_name LIKE '{format_keyword}'")
                    vacancies_with_keyword = cur.fetchall()
        finally:
            conn.close()
            return vacancies_with_keyword

    @staticmethod
    def get_avg_salary():
        """Метод, получающий среднюю зарплату по вакансиям (минимальную и максимальную)"""
        try:
            with psycopg2.connect(host='localhost', database='course_paper_5', user='postgres', password='111111') as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT ROUND(AVG(min_pay)) as avg_min_pay, ROUND(AVG(max_pay)) as avg_max_pay "
                                "FROM vacancies")
                    avg_salary = cur.fetchall()
        finally:
            conn.close()
            return avg_salary

    @staticmethod
    def get_vacancies_with_higher_salary():
        """Метод, получает список всех вакансий, у которых зарплата (минимальная или максимальная) выше средней по всем вакансиям"""
        try:
            with psycopg2.connect(host='localhost', database='course_paper_5', user='postgres', password='111111') as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM vacancies "
                                "WHERE min_pay > (SELECT ROUND(AVG(min_pay)) FROM vacancies) "
                                "OR max_pay > (SELECT ROUND(AVG(max_pay)) FROM vacancies)")
                    vacancies_with_higher_salary = cur.fetchall()
        finally:
            conn.close()
            return vacancies_with_higher_salary
