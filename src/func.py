from src.api_services_classes import *
from src.DB_classes import *
from src.vacansy_class import *


def insert_to_table(employers_list):
    """Функция, заполняющая таблицы вакансиями работодателей из переданного списка"""
    hh_api = HeadHunterAPI()
    for employers in employers_list:
        hh_vacancies = hh_api.get_employer_vacancies(employers)
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
        DBManager.insert_to_table(vacancies_list)
