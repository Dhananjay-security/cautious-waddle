# import requests
# from bs4 import BeautifulSoup
# import json
# from  datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.common.by import By

# url = "https://www.theverge.com/"
# driver = webdriver.Chrome()  # Replace with the path to your chromedriver executable

# driver.get(url)

# # Find all the <a> tags with class="after:absolute after:inset-0 group-hover:shadow-underline-blurple dark:group-hover:shadow-underline-franklin"
# # a_tags = driver.find_elements(By.CSS_SELECTOR, 'a.after\\:absolute.after\\:inset-0.group-hover\\:shadow-underline-blurple.dark\\:group-hover\\:shadow-underline-franklin')
# a_tags1 = driver.find_elements(By.CSS_SELECTOR, 'a.hover\\:shadow-underline-inherit.after\\:absolute.after\\:inset-0')
# a_tags2 = driver.find_elements(By.CSS_SELECTOR, 'a.after\\:absolute.after\\:inset-0.group-hover\\:shadow-underline-blurple.dark\\:group-hover\\:shadow-underline-franklin')


# # Combine the two lists into a single list
# a_tags = a_tags1 + a_tags2

# # Extract the values of the href attributes and store them in a list
# i = 0
# for a_tag in a_tags:
#     url = a_tag.get_attribute('href')
#     if url.startswith('https://www.theverge.com/2023'):
#         r = requests.get(url)
#         i+=1
#         print(i)
#         soup = BeautifulSoup(r.content, 'html.parser')
#         print(url)
#         title = soup.find('meta', property='og:title')['content']
#         print(title) 
#         author = soup.find('meta', {'name': 'parsely-author'})['content']
#         print(author)
#         date = soup.find('meta', {'name': 'parsely-pub-date'})['content']
#         date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
#         formatted_date = date_obj.strftime("%Y/%m/%d")
#         print(formatted_date)


# driver.quit()

# import csv
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.common.by import By

# url = "https://www.theverge.com/"
# driver = webdriver.Chrome()  # Replace with the path to your chromedriver executable

# driver.get(url)

# # Find all the <a> tags with class="after:absolute after:inset-0 group-hover:shadow-underline-blurple dark:group-hover:shadow-underline-franklin"
# a_tags1 = driver.find_elements(By.CSS_SELECTOR, 'a.hover\\:shadow-underline-inherit.after\\:absolute.after\\:inset-0')
# a_tags2 = driver.find_elements(By.CSS_SELECTOR, 'a.after\\:absolute.after\\:inset-0.group-hover\\:shadow-underline-blurple.dark\\:group-hover\\:shadow-underline-franklin')

# # Combine the two lists into a single list
# a_tags = a_tags1 + a_tags2

# # Extract the values of the href attributes and store them in a list
# data = []
# i = 0
# for a_tag in a_tags:
#     url = a_tag.get_attribute('href')
#     if url.startswith('https://www.theverge.com/2023'):
#         r = requests.get(url)
#         i+=1
#         soup = BeautifulSoup(r.content, 'html.parser')
#         title = soup.find('meta', property='og:title')['content']
#         author = soup.find('meta', {'name': 'parsely-author'})['content']
#         date = soup.find('meta', {'name': 'parsely-pub-date'})['content']
#         date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
#         formatted_date = date_obj.strftime("%Y/%m/%d")
#         data.append([i, url, title, author, formatted_date])

# driver.quit()

# # Write data to a csv file
# with open('verge_articles.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['id', 'url', 'title', 'author', 'date'])
#     writer.writerows(data)
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://www.theverge.com/"
driver = webdriver.Chrome()  # Replace with the path to your chromedriver executable

driver.get(url)

# Find all the <a> tags with class="hover:shadow-underline-inherit after:absolute after:inset-0"
a_tags1 = driver.find_elements(By.CSS_SELECTOR, 'a.hover\\:shadow-underline-inherit.after\\:absolute.after\\:inset-0')
a_tags2 = driver.find_elements(By.CSS_SELECTOR, 'a.after\\:absolute.after\\:inset-0.group-hover\\:shadow-underline-blurple.dark\\:group-hover\\:shadow-underline-franklin')

# Combine the two lists into a single list
a_tags = a_tags1 + a_tags2
id = -1
# Extract the values of the href attributes and store them in a list
data = []
for a_tag in a_tags:
    url = a_tag.get_attribute('href')
    if url.startswith('https://www.theverge.com/2023'):
        r = requests.get(url)
        id+=1
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find('meta', property='og:title')['content']
        author = soup.find('meta', {'name': 'parsely-author'})['content']
        date = soup.find('meta', {'name': 'parsely-pub-date'})['content']
        date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date = date_obj.strftime("%Y/%m/%d")
        data.append([id, url, title, author, formatted_date])

driver.quit()
# Write the data to a CSV file
filename = datetime.now().strftime("%d%m%Y") + '_verge.csv'
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'URL', 'Title', 'Author', 'Date'])
    writer.writerows(data)

print(f"Data has been saved to {filename}")

import sqlite3
from datetime import datetime

# Get the current date in the required format
current_date = datetime.today().strftime('%d%m%Y')

# Define the database name
db_name = "verge.db"

# Create a connection to the database
conn = sqlite3.connect(db_name)
c = conn.cursor()

#Creating Table for every YEAR
year = datetime.today().year
table_name = str(year)

# Create table if it doesn't exist
c.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" (id INTEGER PRIMARY KEY, url TEXT UNIQUE, title TEXT, author TEXT, date TEXT)')

# Insert data into the table
for record in data:
    c.execute(f'SELECT id FROM "{table_name}" WHERE id = ?', (record[0],))
    result = c.fetchone()
    if result is None:
        c.execute(f'INSERT INTO "{table_name}" VALUES (?, ?, ?, ?, ?)', record)

# Commit the changes and close the connection
conn.commit()
conn.close()