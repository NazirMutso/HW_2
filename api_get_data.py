from config_f import *
from funcs import get_vacancies_api, get_values_api
from table_maker import Vacancies_data
import time
import random

engine = create_engine(db_name)

flag = 0
num_page = 0
while flag < 100:
    print(f'Парсится страница №{num_page + 1}')
    url = f'https://api.hh.ru/vacancies?page={str(num_page)}'
    for link in get_vacancies_api(url):
        try:
            company, position, job_descrip, key_skills = get_values_api(link)
            new_vac = Vacancies_data(company_names=company,
                                     position=position,
                                     job_description=job_descrip,
                                     key_skills=key_skills)
            time.sleep(random.randrange(6, 10))
            with Session(engine) as session:
                try:  # записываем данные в базуданных
                    session.add(new_vac)
                    session.commit()
                    flag += 1
                    print(f'{flag} вакансия "{position}" компании "{company}" записана в таблицу')
                except:
                    print(f'"{company}" есть в таблице')
        except TypeError:  # бывают страницы не подходящее под условия обработки функции "get_cvdks"
            print('Ошибка: "cannot unpack non-iterable NoneType object"')
            print('Неподходящий формат данных на странице вакансии')
            continue
        if flag == 100:
            print(f'Получено {flag} записей. Программа выполнена')
            break
    num_page += 1  # указываем какую страницу результатом поиска обрабатывать
