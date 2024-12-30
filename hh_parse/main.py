import re
import requests
from bs4 import BeautifulSoup

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


def main():
    respons = requests.get('https://hh.ru/search/vacancy?area=113&schedule=remote&text=python', 
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
        else:
            vacancy_payment = ''
        print(vacancy_payment)

        # experience
        if vacancy.find('span', attrs={"data-qa": re.compile('vacancy-serp__vacancy-work-experience')}):
            vacancy_experience = vacancy.find('span', attrs={"data-qa": re.compile('vacancy-serp__vacancy-work-experience')}).get_text()
            print(vacancy_experience)
        else:
            vacancy_experience = []
        
        if link:
            print(key_requirements(link))

        print('')

if __name__ in "__main__":
    main()