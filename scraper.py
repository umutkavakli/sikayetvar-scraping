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
        self.rows = []


    def change_page(self, brand, complaint=None):
        if complaint is not None:
            next_query = Scraper.__BASE_URL + complaint.find('section').find('h2').find('a').get('href')
        else:
            next_query = Scraper.__BASE_URL + '/' + brand.lower() + Scraper.__QUERY + str(self.page_number)

        next_page = requests.get(next_query, headers=Scraper.__HEADERS)
        return BeautifulSoup(next_page.content, 'html.parser')


    def add_unsolved(self, brand, page_soup):
        unsolved = page_soup.findAll('article', {'class': 'story-card complaint-card ga-v ga-c'})

        for i in range(len(unsolved)):
            complaint_soup = self.change_page(brand, complaint=unsolved[i])
            complaint = complaint_soup.find('article', {'class': 'story-primary complaint-card'})

            data = {
                'brand':           brand,
                'customer_name':   complaint.find('span', {'class': 'username'}).find('a').text,
                'customer_link':   complaint.find('span', {'class': 'username'}).find('a').get('href'),
                'date':            complaint.find('span', {'class': 'username'}).find('span', {'class': 'post-time'}).get('title'),
                'rating':          len(complaint_soup.find('section', {'class': 'post-setting'}).findAll('span', {'class': 'dark-yellow icomoon-full-star'})),
                'is_solved':       False,
                'complaint_title': complaint.find('h1', {'class': 'complaint-title'}).text,
                'complaint_text':  complaint.find('div', {'class': 'card-text'}).text
            }

            self.rows.append(data)
    

    def add_solved(self, brand, page_soup):
        solved = page_soup.findAll('article', {'class': 'story-card complaint-card solved ga-v ga-c'})

        for i in range(len(solved)):
            complaint_soup = self.change_page(brand, complaint=solved[i])
            complaint = complaint_soup.find('article', {'class': 'story-primary complaint-card'})

            data = {
                'brand':           brand,
                'customer_name':   complaint.find('span', {'class': 'username'}).find('a').text,
                'customer_link':   complaint.find('span', {'class': 'username'}).find('a').get('href'),
                'date':            complaint.find('span', {'class': 'username'}).find('span', {'class': 'post-time'}).get('title'),
                'rating':          len(complaint_soup.find('section', {'class': 'post-setting'}).findAll('span', {'class': 'dark-yellow icomoon-full-star'})),
                'is_solved':       True,
                'complaint_title': complaint.find('h1', {'class': 'complaint-title'}).text,
                'complaint_text':  complaint.find('div', {'class': 'card-text'}).text
            }

            self.rows.append(data)


    def scrape_data(self):

        self.exception_counter = 0
        
        for brand in self.brands:
            self.page_number = self.start_page
            
            while self.page_number <= 2:
                next_page_soup = self.change_page(brand)

                try:
                    if self.complaint_type == 'both':
                        self.add_solved(brand, next_page_soup)
                        self.add_unsolved(brand, next_page_soup)
                    elif self.complaint_type == 'solved':
                        self.add_solved(brand, next_page_soup)
                    else:
                        self.add_unsolved(brand, next_page_soup)
                except Exception:
                    self.exception_counter += 1

                self.page_number += 1


    def print_info(self):
        # TODO
        pass


    def save_data(self, path, file_type):
        #TODO
        pass

