import requests
import json
from abc import ABC, abstractmethod


class APIServices(ABC):
    @abstractmethod
    def get_vacancies(self, vacancy_name):
        """Метод, получающий список вакансий по переданному значению"""
        pass

    @abstractmethod
    def get_employer_vacancies(self, employer_name):
        """Метод, получающий список вакансий работодателя"""
        pass


class HeadHunterAPI(APIServices):
    def get_vacancies(self, vacancy_name):
        params = {
            'text': vacancy_name,
            'area': 113,
            'per_page': 100
        }
        req = requests.get('https://api.hh.ru/vacancies', params)
        data = req.content.decode()
        req.close()
        json_data = json.loads(data)
        return json_data

    def get_employer_vacancies(self, employer_name):
        params = {
            'text': employer_name,
            'area': 113,
            'per_page': 100,
            'only_with_vacancies': True
        }
        req = requests.get('https://api.hh.ru/employers', params)
        data = req.content.decode()
        req.close()
        json_data = json.loads(data)
        new_req = requests.get(json_data['items'][0]['vacancies_url'])
        new_data = new_req.content.decode()
        new_req.close()
        new_json_data = json.loads(new_data)
        return new_json_data
