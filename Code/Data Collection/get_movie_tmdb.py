import requests
import csv
from bs4 import BeautifulSoup
import http.client
import json
import urllib.parse
from datetime import datetime as dt


def get_tropes(id,moviename, url):


    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html)
    table = soup.find('div', attrs={'class': 'article-content retro-folders'})
    list_of_movie = []
    list_of_rows = []
    list_of_tropes=[]
    list = table.find('ul')
    for list_trope in table.findAll('li'):
        a = list_trope.findAll('a')
        if len(a) > 0:
            list_of_cells = []
            list_of_cells.append(id)
            list_of_cells.append(moviename)
            trope_title = a[0].contents[0]
            list_of_cells.append(trope_title)
            list_of_rows.append(list_of_cells)
    outfile = open("./movie.csv", "a" , encoding="utf-8",newline='')
    writer = csv.writer(outfile)
    print(list_of_rows)
    writer.writerows(list_of_rows)
    return
def get_tmdb(id,moviename, url):

    print(moviename)
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"
    moviename_encoded= urllib.parse.quote_plus(moviename)
    conn.request("GET","/3/search/movie?include_adult=true&page=1&query="+moviename_encoded+"&language=en-US&api_key=a225706021a10c5976e6223feb6bbb57",payload)
    res = conn.getresponse()
    data = res.read()

    tmdb_data = json.loads(data.decode("utf-8"))
    for tmdb in tmdb_data["results"]:
        with open('movie_tmdb.csv', 'a', encoding="utf-8") as writeFile:
            print(tmdb["original_title"])
            print(tmdb["title"].strip() == moviename.strip())

            if tmdb["title"].strip() == moviename.strip():
                movie_release=''
                if tmdb["release_date"]!='':
                    movie_release = dt.strptime(tmdb["release_date"], "%Y-%m-%d")
                    print(movie_release.year)
                if movie_release!='' and  movie_release.year>=2010 and movie_release.year<=2019:
                    writeFile.writelines(str(id)+","+moviename+","+str(tmdb["id"])+","+str(tmdb["vote_average"])+","+str(tmdb["vote_count"])+","+str(tmdb["vote_average"])+","+str(tmdb["popularity"])+","+str(tmdb["overview"])+"\n")

    return

with open('movie_list_20102014.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    #get_tmdb(1,"Advantageous","ds")
    for row in reader:
        get_tmdb(row[0],row[1],row[2])