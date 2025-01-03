from pathlib import Path
import scrapy
import requests
from bs4 import BeautifulSoup
import re
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

class HhSpider(scrapy.Spider):
    name = "hh"
    start_urls = [
        "https://hh.ru/search/vacancy?area=113&schedule=remote&text=python&salary=100000&only_with_salary=true",
    ]

    def parse(self, response):

        vacancy_list = []
        vacancy_block = response.css('main.vacancy-serp-content')
        for vacancy in vacancy_block.css("div.magritte-redesign"):
            vacancy_list.append(vacancy)
        
        for vacancy in vacancy_list:

            link = vacancy.css("a[data-qa*=serp-item__title]::attr(href)").get()
            print(link)

            # experience
            vacancy_experience = vacancy.css("span").getall()[4]
            vacancy_experience = ' '.join(re.findall(r'\>(.*?)\<', vacancy_experience))
            if not vacancy_experience:
                vacancy_experience = ''
            print(vacancy_experience)

            # vacancy_payment
            vacancy_payment = vacancy.css("span").getall()[3]
            if vacancy_payment:
                vacancy_payment = vacancy_payment.replace('\u202f', '')
                vacancy_payment = ' '.join(re.findall(r'\>(.*?)\<', vacancy_payment))
                vacancy_payment = re.findall(r'\b\d+\b', vacancy_payment)
                vacancy_payment = [int(item) for item in vacancy_payment]
                vacancy_payment = int(sum(vacancy_payment) / len(vacancy_payment))
            else:
                vacancy_payment = 0

            if link:
                keys = key_requirements(link)

            str_v = str(vacancy_experience) +' # '+str(vacancy_payment)+' # '+str(keys)

            with open('scan_result.txt', 'a+', encoding='UTF-8') as f:
                f.write("%s\n" % str_v)

        next_page = response.css('nav a[data-qa*=pager-next]::attr(href)').get()
        if next_page:
            time.sleep(5)
            yield scrapy.Request(url='https://hh.ru'+next_page, callback=self.parse)

        else:
            return