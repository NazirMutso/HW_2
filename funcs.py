from config_f import *


# загружает страницу поиска вакансий с заданными параметрами, возвращает список ссылок на вакансии
def get_links(url):
    headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, '
                  'image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36'
    }
    params = {
        'text': 'middle python developer',
        'area': 113,
        'per_page': 20
    }
    res = requests.get(url, headers=headers, params=params)
    print(f'Статус загрузки страницы поиска: {res.status_code}')
    soup = BeautifulSoup(res.content.decode(), 'lxml')
    vac_link = soup.find_all('a', attrs={'data-qa': 'serp-item__title'})
    links_list = []
    for link in vac_link:
        links_list.append(link.attrs.get('href'))
    return links_list


# Загружает страницу вакансии, возвращает нужные данные со страницы вакансии
# (наз. компании, наз. вакансии, опис. вакансии, ключ. навыки)
def get_values(link):
    headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, '
                  'image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36'
    }
    res = requests.get(link, headers=headers)
    print(f'Статус загрузки страницы вакансии: {res.status_code}')
    soup = BeautifulSoup(res.content.decode(), 'lxml')
    position = soup.find('h1')
    company_name = soup.find('a', attrs={'data-qa': 'vacancy-company-name'})
    job_description = soup.find('div', attrs={'data-qa': 'vacancy-description'})
    key_skills = soup.find_all('span', attrs={'data-qa': 'bloko-tag__text'})
    if key_skills:  # проверка на наличие ключевых навыков в вакансии
        skills = [skill.text for skill in key_skills]
        str_ks = ' '.join(skills)  # создание строки из списка навыков
        data = (company_name.text, position.text, job_description.text, str_ks)
        return data


# загружает API HH с заданными параметрами, возвращает список ссылок на вакансии
def get_vacancies_api(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/114.0.0.0 Safari/537.36'}
    params = {'text': 'meddle python developer',
              'area': 113,
              'per_page': 100}
    res = requests.get(url, headers=headers, params=params)
    print(f'Статус загрузки страницы поиска: {res.status_code}')
    vacancies = res.json().get('items')
    vac_links = []
    for i, vacancy in enumerate(vacancies):
        vac_links.append(vacancy['url'])
    return vac_links


# обрабатывает страницу вакансии, возвращает необходимые данные
def get_values_api(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/114.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers)
    print(f'Статус загрузки страницы вакансии: {res.status_code}')
    vacancy = res.json()
    company_name = vacancy['employer']['name']
    vacancy_name = vacancy['name']
    job_description = vacancy['description']
    key_skills = vacancy['key_skills']
    if key_skills:
        list_ks = [skill['name'] for skill in key_skills]
        str_ks = ' '.join(list_ks)
        data = (company_name, vacancy_name, job_description, str_ks)
        return data
