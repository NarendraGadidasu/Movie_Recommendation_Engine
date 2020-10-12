import requests
from bs4 import BeautifulSoup
import csv
import time


def write_trope_details(trope_url, trope_name):
    # print(trope_url, trope_name)
    content = ""
    try:
        if "https://tvtropes.org" in trope_url:
            response = requests.get(trope_url)
        else:
            response = requests.get(f"https://tvtropes.org{trope_url}")
    except Exception as e:
        print(f"Skipped trope: {trope_url}")
        return
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    start = soup.find("div", {"id": "main-article"})
    end = start.find("h2")
    if not end:
        end = start.find("h1")
        if not end:
            end = start.find_next_sibling("div")
    try:
        item = start.next_element
        while item != end:
            if item.name == "p":
                content += f"{item.text}##"
            elif item.name == "ul":
                content += f"{item.text}##"
            item = item.next_element
        writer.writerow([trope_name, trope_url, content])
    except Exception as e:
        print(f"Skipped trope: {trope_url}")
        return
    # print([trope_name, trope_url, content])

def extract_trope_link(movie_url):
    print(f"Movie URL: {movie_url}")
    try:
        response = requests.get(movie_url)
    except Exception as e:
        print(f"Skipping movie: {movie_url}")
        return
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    start = soup.find("div", {"id": "main-article"})
    target = start.find_all("h2")
    if len(target) == 0:
        target = start.find_all("h1")
        if len(target)==0:
            print(f"Skipping movie: {movie_url}")
            return
    sibling = target[0]
    found = False
    while (not found) and bool(sibling):
        sibling = sibling.find_next_sibling()
        # print(sibling.name)
        try:
            if sibling.name == "ul":
                found = True
        except Exception as e:
            continue
    try:
        ini_element = sibling.next_element
        # print(f"Initial element : {ini_element}")
        list_elements = [ini_element]
        for element in ini_element.find_next_siblings():
            if element.name == "li":
                list_elements.append(element)
        trope_details = {}
        for list_element in list_elements:
            # print(f"list_element : {list_element}")
            try:
                tag = list_element.find_all("a")[0]
                # print(f"Tag: {tag.get('href')}")
                trope_link = tag.get("href")
                trope_name = tag.text
                # print(f"{trope_name}, {trope_link}")
                if trope_link not in tropes:
                    write_trope_details(trope_link, trope_name)
                    tropes.add(trope_link)
            except Exception as e:
                print(f"Error in element: {list_element}")
                continue
    except Exception as e:
        print(f"Skipping movie: {movie_url}")

#
tropes = set()
final_file = open("trope_details.csv", "a", encoding="utf-8")
writer = csv.writer(final_file)
row_num = 0
try:
    with open("movie_list.txt", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row_num % 10 == 0:
                print(f"{row_num} movie tropes scraped")
            url = row[1]
            if row_num > -1:
                extract_trope_link(url)
                final_file.flush()
                time.sleep(2)
            row_num += 1
except Exception as e:
    print(f"{str(e)}")
final_file.close()

# if __name__ == "__main__":
#     write_trope_details("https://tvtropes.org/pmwiki/pmwiki.php/Main/Adorkable", "Adorkable")