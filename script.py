import sys
import csv
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
from urllib.request import urlparse


class Implementation:
    filename = str()
    answers = 'wikipedia_answers_example.csv'
    pages = list()
    column_name = ('wikipedia_page', 'website')

    @classmethod
    def check_answer_file(cls):
        try:
            cls.filename = sys.argv[1]
        except IndexError:
            exit()

    @classmethod
    def get_data(cls):
        cls.check_answer_file()
        try:
            with open(cls.filename) as data_file:
                for row in csv.reader(data_file):
                    cls.pages.extend(row)
        except FileNotFoundError:
            exit()

    @classmethod
    def record(cls, data_for_read):
        with open(cls.answers, 'a') as data_file:
            writer = csv.writer(data_file)
            writer.writerow(data_for_read)

    @classmethod
    def process(cls):
        cls.get_data()
        cls.record(cls.column_name)
        for wikipedia_page_url in cls.pages:
            try:
                doc = urlopen(wikipedia_page_url).read()
            except urllib.request.HTTPError:
                break
            else:
                html = BeautifulSoup(doc, 'html.parser')
                try:
                    get_url = html.find('th', text='Website').parent.find('a')['href']
                    website_url = get_url if urlparse(get_url).scheme else 'http:{}'.format(get_url)
                except AttributeError:
                    website_url = 'Site Not Found!'
                full_data = (wikipedia_page_url, website_url)
                cls.record(full_data)

Implementation.process()
