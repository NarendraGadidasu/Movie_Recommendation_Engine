import requests
import csv
from bs4 import BeautifulSoup


def get_tropes(moviename, url):
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html)
    table = soup.find('div', attrs={'class': 'article-content retro-folders'})
    list_of_movie = []
    list_of_rows = []
    list = table.find('ul')
    # list_of_rows.append(['Movie', 'Trope'])
    for list_trope in table.findAll('li'):
        a = list_trope.findAll('a')
        if len(a) > 0:
            list_of_cells = []
            list_of_cells.append(moviename)
            trope_title = a[0].contents[0]
            list_of_cells.append(trope_title)
            list_of_rows.append(list_of_cells)
    # print(list_of_rows)
    with open("./movie_20102014.csv", "a", encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(list_of_rows)
    return

with open('movie_list_20102014.txt', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    row_num = 0
    for row in reader:
        get_tropes(row[0], row[1])
        print(f"{row_num} movies done!")
        row_num += 1
