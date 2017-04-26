import sys
import csv
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
from urllib.request import urlparse
from multiprocessing import Pool


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
    def make_all(cls, url):
        try:
            doc = urlopen(url).read()
        except urllib.request.HTTPError:
            website_url = 'No info found'
        else:
            html = BeautifulSoup(doc, 'html.parser')
            try:
                get_url = html.find('th', text='Website').parent.find('a')['href']
                website_url = get_url if urlparse(get_url).scheme else 'http:{}'.format(get_url)
            except AttributeError:
                website_url = 'Site Not Found!'
        full_data = (url, website_url)
        cls.record(full_data)

    @classmethod
    def process(cls):
        cls.get_data()
        cls.record(cls.column_name)
        with Pool(8) as p:
            p.map(cls.make_all, cls.pages)

Implementation.process()
