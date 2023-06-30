from bs4 import BeautifulSoup
import os
import requests

#####################################################
# Extracting the links of multiple movie transcripts
#####################################################

# How To Get The HTML
root = 'https://subslikescript.com'  # this is the homepage of the website
website = f'{root}/movies'  # concatenating the homepage with the movies section
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())  # prints the HTML of the website

# Locate the box that contains a list of movies
box = soup.find('article', class_='main-article')

# Store each link in "links" list (href doesn't consider root aka "homepage", so we have to concatenate it later)
links = []
for link in box.find_all('a', href=True):  # find_all returns a list
    links.append(link['href'])

print(links)
#################################################
# Extracting the movie transcript
#################################################

# Loop through the "links" list and sending a request to each link
for link in links:
    result = requests.get(f'{root}/{link}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    for e in soup.select('article', class_='main-article'):
        name = e.h1.get_text(strip=True)
        html = e.find('div', class_='full-script').get_text(strip=True, separator=' ')

        try:
            with open(f'{name}.txt', 'w', encoding='utf-8') as file:
                file.write(html)
                file.close()
        except Exception as e:
            print(e)