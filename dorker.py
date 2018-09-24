# -*- coding: utf-8 -*-
# Author: https://github.com/theShaswato
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup as bs
from sys import exit, argv
import requests, urllib.parse

header = {'user-agent': 'Moofzilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
url1 = "https://bing.com/search?q="

class Dorker(object):

    urls = []

    def __init__(self, dorks, page_count, thread_count):
        self.dorks = dorks
        self.page_count = page_count
        self.thread_count = thread_count

    def makelist(self, dork):
        i = page = 1
        while i <= self.page_count:
            url = url1 + urllib.parse.quote(dork) + '&first=' + str(page)
            self.urls.append(url)
            i += 1
            page += 10

    def load(self, url):
        html = requests.get(url, headers = header).text
        data = bs(html, 'html.parser')
        results = data.find('ol', {'id': 'b_results'})
        results = results.find_all('li', {'class': 'b_algo'})
        for result in results:
            link = result.find('a').attrs['href']
            print(link)
            f = open('found.html', 'a')
            f.write('<a style="text-decoration:none" href="{}">{}</a><br>\n'.format(link, link))
            f.close()

    def run(self):
        for dork in self.dorks:
            self.makelist(dork)
            with Pool(self.thread_count) as worker:
                worker.map(self.load, self.urls)
                worker.close()
                worker.join()
            self.urls = []

def main():

    dorks = thread_count = page_count = None

    if len(argv) > 1:
        if argv[1].lower() == 'file':
            try:
                dorks = open(input("Enter dorklist file path: "), 'r').read().split('\n')
            except IOError:
                exit("Dorklist not found")
        else:
            exit("Error, unknown option")
    else:
        dorks = input("Enter your dorks: ").split(' ')

    page_count = int(input("Enter pages to look: "))
    thread_count = int(input("Threads: "))

    open('found.html', 'w').close()

    dorker = Dorker(dorks, page_count, thread_count)
    dorker.run()

    exit("\nDone, results saved in 'found.html'")

if __name__ == '__main__':
    main()