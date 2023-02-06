import requests
import pandas as pd
from bs4 import BeautifulSoup

class Scraper:

    __HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})

    __BASE_URL = 'https://www.sikayetvar.com'
    __QUERY = '?page='

    def __init__(self, brands, complaint_type, start_page, end_page):
        self.brands = brands
        self.complaint_type = complaint_type
        self.start_page = start_page
        self.end_page = end_page
        
    def scrape_data(self):
        
        for brand in self.brands:
            page_number = self.start_page

            rows = []
            
            while page_number <= 2:
                next_page = Scraper.__BASE_URL + '/' + brand.lower() + Scraper.__QUERY + str(self.start_page)
                brand_page = requests.get(next_page, headers=Scraper.__HEADERS)
                soup = BeautifulSoup(brand_page.content, 'html.parser')

                unsolved = soup.findAll('article', {'class': 'story-card complaint-card ga-v ga-c'})

                for i in range(len(unsolved)):

                    try:
                        complaint_link = Scraper.__BASE_URL + unsolved[i].find('section').find('h2').find('a').get('href')
                        complaint_page = requests.get(complaint_link, headers=Scraper.__HEADERS)
                        complaint_soup = BeautifulSoup(complaint_page.content, "html.parser")

                        complaint = complaint_soup.find('article', {'class': 'story-primary complaint-card'})

                        data = {
                            'customer_name':   complaint.find('span', {'class': 'username'}).find('a').text,
                            'customer_link':   complaint.find('span', {'class': 'username'}).find('a').get('href'),
                            'date':            complaint.find('span', {'class': 'username'}).find('span', {'class': 'post-time'}).get('title'),
                            'rating':          len(complaint_soup.find('section', {'class': 'post-setting'}).findAll('span', {'class': 'dark-yellow icomoon-full-star'})),
                            'complaint_title': complaint.find('h1', {'class': 'complaint-title'}).text,
                            'complaint_text':  complaint.find('div', {'class': 'card-text'}).text
                        }

                        rows.append(data)
                        
                    except Exception:
                        #TODO
                        pass

                page_number += 1

            


    def print_info(self):
        # TODO
        pass


    def save_data(self, path, file_type):
        #TODO
        pass

