from logger_conf import my_logger
import asyncio
from aiohttp import ClientSession, TCPConnector
from config_f import *
from table_maker import Vacancies_api, db_name

url_api = 'https://api.hh.ru/vacancies/'


def get_ids(url, page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/114.0.0.0 Safari/537.36'}
    params = {'text': 'meddle python developer',
              'search_field': 'name',
              'area': 113,
              'per_page': 100,
              'page': page}
    response = requests.get(url, headers=headers, params=params)
    vacancies = response.json()
    vac_links = [vacancy['id'] for i, vacancy in enumerate(vacancies.get('items'))]
    return vac_links


async def get_vacancy(id, session):
    url = f'/vacancies/{id}'
    my_logger.info(f'Начата загрузка вакансии {url}')
    async with session.get(url=url) as response:
        vacancy_json = await response.json()
        my_logger.info(f'Завершена загрузка вакансии {url}')
        return vacancy_json


async def pars_master_2000(url, database, table, func1, func2):
    engine = create_engine(database)
    flag = 0  # счетчик записанных вакансий
    num_page = 0  # страница поиска вакансий
    while flag < 100:  # цикл на обработку 100 вакансий
        my_logger.debug(f'Парсится страница поиска №{num_page + 1}')
        ids = func1(url, num_page)
        for id in ids:  # функция возвращает список ссылок на вакансии, цикл перебирает их
            connector = TCPConnector(limit=5)
            async with ClientSession('https://api.hh.ru/', connector=connector) as session:
                tasks = []
                tasks.append(asyncio.create_task(func2(id, session)))
                results = await asyncio.gather(*tasks)
            for result in results:
                try:
                    if result['key_skills']:
                        skills_list = [skill['name'] for skill in result['key_skills']]
                        new_vac = table(vacancy_id=result['id'],
                                        company_names=result['employer']['name'],
                                        position=result['name'],
                                        job_description=result['description'],
                                        key_skills=' '.join(skills_list))
                        with Session(engine) as session:  # открываем базу данных
                            try:  # записываем в базу данных
                                session.add(new_vac)
                                session.commit()
                                flag += 1  # добавляем к счетчику вакансий
                                my_logger.info(f'Вакансия "{result["id"]}" компании "{result["employer"]["name"]}" записана в таблицу')
                            except sqlalchemy.exc.IntegrityError:  # если такая компания уже есть в списке
                                my_logger.error(f'Вакансия ID: {result["id"]} "{result["position"]}" уже есть в таблице')
                    else:
                        my_logger.info(f'Не указаны ключевые навыки в вакансии {result["id"]}')
                except KeyError:
                    my_logger.error(f'Неподходящий формат данных на странице вакансии {result["id"]}')
            if flag == 100:  # условие на остановку цикла
                my_logger.info(f'Записано {flag} вакансий. Программа выполнена')
                break
        time.sleep(random.randrange(3, 6))
        num_page += 1  # указываем какую страницу результатов поиска обрабатывать


start = time.time()
asyncio.run(pars_master_2000(url_api, db_name, Vacancies_api, get_ids, get_vacancy))
print(time.time() - start)
