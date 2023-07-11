from config_f import *
from logger_conf import my_logger


# загружает страницу поиска вакансий с заданными параметрами, возвращает список ссылок на вакансии
def get_links(url, page):
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36'
    }
    params = {
        'text': 'middle python developer',
        'search_field': 'name',
        'area': 113,
        'per_page': 50,
        'page': page
    }
    res = requests.get(url, headers=headers, params=params)
    my_logger.info(f'Статус загрузки страницы поиска: {res.status_code}')
    soup = BeautifulSoup(res.content.decode(), 'lxml')
    links = json.loads(soup.find('noindex').string)["vacancySearchResult"]["vacancies"]
    links_list = [link['links']['desktop'] for link in links]
    return links_list


# Загружает страницу вакансии, возвращает нужные данные со страницы вакансии
# (наз. компании, наз. вакансии, опис. вакансии, ключ. навыки)
def get_values(link):
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36'
    }
    res = requests.get(link, headers=headers)
    my_logger.info(f'Статус загрузки страницы вакансии: {res.status_code}')
    soup = BeautifulSoup(res.content.decode(), 'lxml')
    vac_id = soup.find('input', attrs={'name': 'vacancyId'})
    position = soup.find('h1')
    company_name = soup.find('a', attrs={'data-qa': 'vacancy-company-name'})
    job_description = soup.find('div', attrs={'data-qa': 'vacancy-description'})
    key_skills = soup.find_all('span', attrs={'data-qa': 'bloko-tag__text'})
    if key_skills:  # проверка на наличие ключевых навыков в вакансии
        skills = [skill.text for skill in key_skills]
        str_ks = ' '.join(skills)  # создание строки из списка навыков
        try:
            data = (int(vac_id.attrs['value']), company_name.text, position.text, job_description.text, str_ks)
            return data
        except AttributeError:
            my_logger.error('Не указано название компании')


# загружает API HH с заданными параметрами, возвращает список ссылок на вакансии
def get_vacancies_api(url, page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/114.0.0.0 Safari/537.36'}
    params = {'text': 'meddle python developer',
              'search_field': 'name',
              'area': 113,
              'per_page': 100,
              'page': page}
    res = requests.get(url, headers=headers, params=params)
    my_logger.info(f'Статус загрузки страницы вакансии: {res.status_code}')
    vacancies = res.json().get('items')
    vac_links = [vacancy['url'] for i, vacancy in enumerate(vacancies)]
    return vac_links


# обрабатывает страницу вакансии, возвращает необходимые данные
def get_values_api(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/114.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers)
    my_logger.info(f'Статус загрузки страницы вакансии: {res.status_code}')
    vacancy = res.json()
    vac_id = vacancy['id']
    company_name = vacancy['employer']['name']
    vacancy_name = vacancy['name']
    job_description = vacancy['description']
    key_skills = vacancy['key_skills']
    if key_skills:
        list_ks = [skill['name'] for skill in key_skills]
        str_ks = ' '.join(list_ks)
        data = (vac_id, company_name, vacancy_name, job_description, str_ks)
        return data


# main функция, принимает аргументы: адрес, путь к БД, имя таблицы, функцию обработки страницы поиска вакансий,
# функцию получение данных вакансии
def pars_master_2000(url, database, table, func1, func2):
    engine = create_engine(database)
    flag = 0  # счетчик записанных вакансий
    num_page = 0  # страница вакансии
    while flag < 100:  # цикл на обработку 100 вакансий
        my_logger.info(f'Парсится страница поиска №{num_page + 1}')
        # url = url+str(num_page)
        for link in func1(url, num_page):  # функция возвращает список ссылок на вакансии, цикл перебирает их
            try:  # попытка записать данные в таблицу
                vac_id, company, position, job_descrip, key_skills = func2(link)  # функция возвращает кортеж с данными
                # подготавливаем данные для передачи в таблицу
                new_vac = table(vacancy_id=vac_id,
                                company_names=company,
                                position=position,
                                job_description=job_descrip,
                                key_skills=key_skills)
                # time.sleep(random.randrange(3, 6))  # пауза, чтобы не получить бан
                with Session(engine) as session:  # открываем базу данных
                    try:  # записываем в базу данных
                        session.add(new_vac)
                        session.commit()
                        flag += 1  # добавляем к счетчику вакансий
                        my_logger.info(f'{flag} вакансия "{position}" компании "{company}" записана в таблицу')
                    except sqlalchemy.exc.IntegrityError:  # если такая компания уже есть в списке
                        my_logger.error(f'Вакансия ID: {vac_id} "{position}" уже есть в таблице')
            except TypeError:  # бывают страницы не подходящее под условия обработки функции получения данных о вакансии
                my_logger.error('Неподходящий формат данных на странице вакансии')
                continue
            if flag == 100:  # условие на остановку цикла
                my_logger.info(f'Записано {flag} вакансий. Программа выполнена')
                break
        time.sleep(random.randrange(3, 6))
        num_page += 1  # указываем какую страницу результатов поиска обрабатывать
