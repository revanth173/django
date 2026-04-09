import requests
from bs4 import BeautifulSoup
def scrape_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No Title found'
        print(f'Title: {title}')
        links = soup.find_all('a', href=True)
        for link in links: print(link['href'])
    else: print(f'Failed: {response.status_code}')
scrape_webpage("https://www.gmail.com")