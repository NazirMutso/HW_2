# import random
# import time
from config_f import *
from funcs import get_links, get_values
from table_maker import Vacancies_data

engine = create_engine(db_name)

flag = 0
page_numb = 0  # номер страницы поиска
while flag < 100:  # цикл на 100 записей
    print(f'Парсится страница №{page_numb + 1}')
    url = f'https://hh.ru/search/vacancy?page={str(page_numb)}'
    for link in get_links(url):  # цикл для обработки ссылок вакансий со страницы поиска
        try:  # извлекаем данные со страницы вакансии
            company, posit, job_descrip, key_skill = get_values(link)  # функция извлекает нужные данные
            new_vac = Vacancies_data(company_names=company,
                                     position=posit,
                                     job_description=job_descrip,
                                     key_skills=key_skill)
            # time.sleep(random.randrange(6, 10))
            with Session(engine) as session:
                try:  # записываем данные в базуданных
                    session.add(new_vac)
                    session.commit()
                    flag += 1
                    print(f'{flag} вакансия "{posit}" компании "{company}" записана в таблицу')
                except:
                    print(f'"{company}" есть в таблице')
        except TypeError:  # бывают страницы не подходящее под условия обработки функции "get_cvdks"
            print('Ошибка: "cannot unpack non-iterable NoneType object"')
            print('Неподходящий формат данных на странице вакансии')
            continue
        if flag == 100:  # останавливает цикл на 100 записях
            print(f'Получено {flag} записей. Программа выполнена')
            break
    page_numb += 1  # указываем какую страницу результатом поиска обрабатывать
