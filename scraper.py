import os
import time
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

    def __init__(self, brands, start_page, end_page, info, file_extension, output_path):
        self.brands = brands
        self.start_page = start_page
        self.end_page = end_page
        self.info = info
        self.file_extension = file_extension
        self.output_path = output_path
        self.rows = []

    def change_page(self, brand, page_number):
        """
        Returns the soup of brand page in current page number.
        """

        next_query = Scraper.__BASE_URL + '/' + brand.lower() + Scraper.__QUERY + str(page_number)
        next_page = requests.get(next_query, headers=Scraper.__HEADERS)
        return BeautifulSoup(next_page.content, 'html.parser')
    
    def change_complaint_card(self, complaint):
        """
        Returns the soup of indiviual complaint page to access the detail of complaint. 
        """

        complaint_query = Scraper.__BASE_URL + complaint.find('section').find('h2').find('a').get('href')
        complaint_page = requests.get(complaint_query, headers=Scraper.__HEADERS)
        return BeautifulSoup(complaint_page.content, 'html.parser')

    def add_data(self, brand, page_soup):
        """
        Adding all data for current page soup's all customer complaints. 
        """

        complaint_cards = page_soup.findAll('article', {'class': 'story-card complaint-card ga-v ga-c'})

        for i in range(len(complaint_cards)):
            try:
                complaint_soup = self.change_complaint_card(complaint_cards[i])
                complaint = complaint_soup.find('article', {'class': 'story-primary complaint-card'})

                data = {
                    'brand':           brand,
                    'customer_name':   complaint.find('span', {'class': 'username'}).find('a').text,
                    'customer_link':   complaint.find('span', {'class': 'username'}).find('a').get('href'),
                    'date':            complaint.find('span', {'class': 'username'}).find('span', {'class': 'post-time'}).get('title'),
                    'rating':          len(complaint_soup.find('section', {'class': 'post-setting'}).findAll('span', {'class': 'dark-yellow icomoon-full-star'})),
                    'complaint_title': complaint.find('h1', {'class': 'complaint-title'}).text,
                    'complaint_text':  complaint.find('div', {'class': 'card-text'}).text
                }

                self.rows.append(data)
                time.sleep(.5)
            except Exception as exception:
                self.exception_counter += 1
                pass

    def scrape_data(self):
        """
        Controls current brand name for scraping and changes page number.
        It also prints information about scraping if argument is passed.
        """

        self.exception_counter = 0
        
        for brand in self.brands:
            page_number = self.start_page

            while page_number <= self.end_page:

                if self.info:
                    self.print_info(brand, page_number)

                next_page_soup = self.change_page(brand, page_number)
                self.add_data(brand, next_page_soup)

                page_number += 1

            print(f'Number of exceptions: {self.exception_counter}')
        
        self.save_data()

    def print_info(self, brand, page_number):
        print(f'For \"{brand}\" brand, page {page_number} is processing...')
        print(f'Current total number of complaints scraped: {len(self.rows)}\n')
        

    def save_data(self):
        """
        Saves scraped data to desired format (csv or excel) for output path.
        If any location or extension is not passed, then default ones are used ('./' and 'csv').
        It also creates directory for given path if the directory is not created yet.
        """
        # create pandas frame to save data 
        df = pd.DataFrame(self.rows)

        # separate the directory name and file name
        directory_name, file_name = os.path.split(self.output_path)

        # check if directory exists
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        try:
            if self.file_extension == 'csv':
                df.to_csv(os.path.join(directory_name, file_name + ".csv"), index=False)
            else:
                df.to_excel(os.path.join(directory_name, file_name + ".xlsx"), index=False)
            print("Successfully saved.")
        except Exception as err:
            print("Couldn't saved for unexpected reason.")
        

