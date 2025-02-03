import re
import requests
from bs4 import BeautifulSoup
import time

def key_requirements(link: str) -> list[str]:
    respons = requests.get(link, 
                           headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'})
    
    soup = BeautifulSoup(respons.text, 'html.parser')
    vacancy_skill_ul = soup.find('ul', re.compile('vacancy-skill-list'))

    vacancy_skill_list = []
    if vacancy_skill_ul:
        for vacancy_skill_item in vacancy_skill_ul:
            vacancy_skill_list.append(vacancy_skill_item.get_text())

    return vacancy_skill_list


def scan_page(link: str)->list['str']:

    respons = requests.get(link, 
                           headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'})
    
    soup = BeautifulSoup(respons.text, 'html.parser')
    vacancy_block = soup.find('main', class_='vacancy-serp-content')
    vacancy_list = vacancy_block.find_all(class_ = "magritte-redesign")

    
    for vacancy in vacancy_list:

        # link
        link = vacancy.find('a', attrs={"data-qa": re.compile('serp-item__title')})['href']
        print(link)

        # vacancy_payment
        compensation = vacancy.find('div', re.compile('compensation-labels'))
        if compensation.find('span', re.compile('magritte-text')):
            vacancy_payment = compensation.find('span', re.compile('magritte-text')).get_text().replace('\u202f', '')
            vacancy_payment = re.findall(r'\b\d+\b', vacancy_payment)
            vacancy_payment = [int(item) for item in vacancy_payment]
            vacancy_payment = int(sum(vacancy_payment) / len(vacancy_payment))
        else:
            vacancy_payment = 0
        print(vacancy_payment)

        # experience
        if vacancy.find('span', attrs={"data-qa": re.compile('vacancy-serp__vacancy-work-experience')}):
            vacancy_experience = vacancy.find('span', attrs={"data-qa": re.compile('vacancy-serp__vacancy-work-experience')}).get_text()
            print(vacancy_experience)
        else:
            vacancy_experience = []
        
        if link:
            print(key_requirements(link))

        str_v = str(vacancy_experience) +'# '+str(vacancy_payment)+'# '+str(key_requirements(link))

        with open('scan_result.txt', 'a+', encoding='UTF-8') as f:
            f.write("%s\n" % str_v)

    if soup.find('a', attrs={"data-qa": re.compile('pager-next')}):
        next_page_scan = soup.find('a', attrs={"data-qa": re.compile('pager-next')})['href']
        print('Идёт дальше...')
        print(next_page_scan)
        time.sleep(5)
        scan_page('https://hh.ru'+next_page_scan)
    else:
        return


def main():
    link_page_scan = 'https://hh.ru/search/vacancy?area=113&schedule=remote&text=python&salary=100000&only_with_salary=true'

    scan_page(link_page_scan)

    print('Просканили все страницы...')
    print('Переходим к обработке...')
    time.sleep(10)

    with open('scan_result.txt', 'r', encoding='UTF-8') as file:
        vacancy_result = [line.split('#') for line in file]
    
    
    vacancy_dict = {}
    for vacancy_item in vacancy_result:
        if vacancy_dict.get(vacancy_item[0]) is not None:
            vacancy_dict[vacancy_item[0]].append(vacancy_item[1])
            vacancy_dict[vacancy_item[0]].append(vacancy_item[2])
        else:
            vacancy_dict[vacancy_item[0]] = []
            vacancy_dict[vacancy_item[0]].append(vacancy_item[1])
            vacancy_dict[vacancy_item[0]].append(vacancy_item[2])

    vacancy_result = dict(sorted(vacancy_dict.items()))
    print(vacancy_result)


if __name__ in "__main__":
    main()