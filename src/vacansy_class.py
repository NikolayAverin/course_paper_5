class Vacancy:
    def __init__(self, name, url, area, requirement, min_pay, max_pay, currency, employer):
        self.name = name
        self.url = url
        self.min_pay = min_pay
        self.max_pay = max_pay
        self.area = area
        self.requirement = requirement
        self.currency = currency
        self.employer = employer
        # if self.requirement is None:
        #     self.requirement = ''
        # if self.min_pay is None:
        #     self.min_pay = 0
        # if self.max_pay is None:
        #     self.max_pay = 0

    def __str__(self):
        if self.min_pay == 0 and self.max_pay == 0:
            return f'{self.name}, зарплата не указана, в {self.area}, ссылка {self.url}'
        elif self.min_pay == 0:
            return f'{self.name}, зарплата до {self.max_pay} {self.currency}, в {self.area}, ссылка {self.url}'
        elif self.max_pay == 0:
            return f'{self.name}, зарплата от {self.min_pay} {self.currency}, в {self.area}, ссылка {self.url}'
        else:
            return (f'{self.name}, зарплата: {self.min_pay} - {self.max_pay} {self.currency}, в {self.area}, '
                    f'ссылка {self.url}')

    def __repr__(self):
        if self.min_pay == 0 and self.max_pay == 0:
            return f'{self.name}, зарплата не указана, в {self.area}, ссылка {self.url}'
        elif self.min_pay == 0:
            return f'{self.name}, зарплата до {self.max_pay} {self.currency}, в {self.area}, ссылка {self.url}'
        elif self.max_pay == 0:
            return f'{self.name}, зарплата от {self.min_pay} {self.currency}, в {self.area}, ссылка {self.url}'
        else:
            return (f'{self.name}, зарплата: {self.min_pay} - {self.max_pay} {self.currency}, в {self.area}, '
                    f'ссылка {self.url}')

    def __lt__(self, other):
        result = self.max_pay < other.max_pay
        return result

    @staticmethod
    def cast_to_object_list(data):
        """Метод, создающий список экземпляров класса из переданного списка вакансий"""
        vacancies_list = []
        for item in data['items']:
            if item['salary'] is None:
                item['salary'] = {'from': None, 'to': None, 'currency': ''}
            vacancies_list.append(
                Vacancy(item['name'], item['url'], item['area']['name'], item['snippet']['requirement'],
                        item['salary']['from'], item['salary']['to'], item['salary']['currency'],
                        item['employer']['name']))
        return vacancies_list

    @staticmethod
    def filter_keyword_vacancies(vacancies_list, filter_words):
        """Метод, возвращающий отсортированный по ключевым словам список экземпляров класса"""
        filtered_vacancies = []
        formated_filter_words = Vacancy.get_format_list(filter_words)
        for vacancy in vacancies_list:
            vacancy_words = f'{vacancy.area.lower()} {vacancy.name.lower()} {vacancy.requirement.lower()}'
            formated_vacancies_list = Vacancy.get_format_list(vacancy_words)
            if set(formated_filter_words).issubset(formated_vacancies_list):
                filtered_vacancies.append(vacancy)
        return filtered_vacancies

    @staticmethod
    def get_format_list(data_to_format):
        """Метод, возвращающий входящие данные в формате, подходящем для фильтрации"""
        alpha_str = ''
        for symbol in data_to_format:
            if symbol.isalpha() or symbol == ' ':
                alpha_str += symbol
            else:
                alpha_str += ' '
        alpha_list = alpha_str.split(' ')
        result_list = []
        for word in alpha_list:
            if word != '':
                result_list.append(word)
        return result_list

    @staticmethod
    def filter_min_salary(filtered_vacancies, min_salary):
        """Метод, возвращающий экземпляры класса, отфильтрованные по минимальной зарплате"""
        filtered_min_salary_vacancies = []
        for vacancy in filtered_vacancies:
            if vacancy.min_pay >= min_salary:
                filtered_min_salary_vacancies.append(vacancy)
        return filtered_min_salary_vacancies

    @staticmethod
    def filter_max_salary(filtered_vacancies, max_salary):
        """Метод, возвращающий экземпляры класса, отфильтрованные по максимальной зарплате"""
        filtered_max_salary_vacancies = []
        for vacancy in filtered_vacancies:
            if vacancy.max_pay <= max_salary:
                filtered_max_salary_vacancies.append(vacancy)
        return filtered_max_salary_vacancies
