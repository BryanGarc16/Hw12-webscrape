from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import matplotlib.pyplot as plt

my_driver = webdriver.Chrome()
my_driver.set_page_load_timeout(60)
my_driver.get("https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States")

wait = WebDriverWait(my_driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.wikitable")))

table_soup = BeautifulSoup(my_driver.page_source, "html.parser")
table = table_soup.find("table", class_="wikitable")

inner_table = table.find("tbody")

pres_links = []

for row in inner_table.find_all("tr"):
    columns = row.find_all("td")
    if len(columns) > 2:
        b_tag = columns[1].find("b")
        if b_tag:
            link_tag = b_tag.find("a")
            if link_tag and "href" in link_tag.attrs:
                full_url = "https://en.wikipedia.org" + link_tag["href"]
                pres_links.append(full_url)

pres_dict = {}
for link in pres_links:
    my_driver.get(link)
    #time.sleep(.5)
    soup = BeautifulSoup(my_driver.page_source, "html.parser")
    pres_name = soup.find("h1", id="firstHeading").text
    pres_dict[pres_name] = 0

    paragraphs = soup.find_all("p")
    for paragraph in paragraphs:
        if "war" in paragraph.text.lower():
           pres_dict[pres_name] += 1
my_driver.quit()

sorted_pres = sorted(pres_dict.items(), key=lambda item: item[1], reverse=True)
print(len(sorted_pres))
print(sorted_pres)

for pres, num in sorted_pres:
    print(f"{pres}: {num}")

x_vals = [ii for ii in range(len(pres_dict.keys()))]
y_vals = [num for pres, num in pres_dict.items()]
plt.plot(x_vals, y_vals)
plt.annotate("Grant", xy=(x_vals[18], y_vals[18]))
plt.annotate("Truman", xy=(x_vals[33], y_vals[33]))
plt.annotate("Lincoln", xy=(x_vals[17], y_vals[17]))
plt.annotate("Nixon", xy=(x_vals[37], y_vals[37]))
plt.show()



