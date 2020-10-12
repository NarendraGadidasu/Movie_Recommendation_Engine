from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import csv

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
browser = webdriver.Chrome(executable_path="/Users/kunalsingh/Downloads/Softwares/chromedriver", chrome_options=option)

browser.get("https://tvtropes.org/pmwiki/pmwiki.php/Main/FilmsOf20102014")

timeout = 5
try:
    WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located(
            (By.ID, "main-article")
        )
    )
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

print("Page Loaded!")

# find_elements_by_xpath returns an array of selenium objects.
content = browser.find_element_by_id("main-article")
content.find_element_by_class_name("toggle-all-folders-button").click()
# use list comprehension to get the actual repo titles and not the selenium objects.
with open("movie_list_20102014.txt", "w") as wf:
    links = content.find_elements_by_tag_name("em")
    print(len(links))
    for link in links:
        try:
            result = link.find_element_by_class_name("twikilink")
            # wf.write(f"{result.text},{result.get_property('href')}\n")
            writer = csv.writer(wf)
            writer.writerow([result.text, result.get_property('href')])
        except Exception as e:
            continue
# # print out all the titles.
# print('titles:')
# print(titles, '\n')
browser.quit()

