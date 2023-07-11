from table_maker import Vacancies_pars, Vacancies_api, db_name
from funcs import get_links, get_values, get_vacancies_api, get_values_api, pars_master_2000

url = 'https://hh.ru/search/vacancy?page='
url_api = 'https://api.hh.ru/vacancies?page='

# парсинг WEB-страниц
pars_master_2000(url, db_name, Vacancies_pars, get_links, get_values)

# получение данных с API
pars_master_2000(url_api, db_name, Vacancies_api, get_vacancies_api, get_values_api)
