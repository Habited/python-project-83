import requests
from bs4 import BeautifulSoup


def parser(url):
    response = requests.get(url["name"], timeout=5)
    response.raise_for_status()
    status_code = response.status_code

    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.h1.get_text().strip() if soup.h1 else ''
    title = soup.title.string.strip() if soup.title else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag.get(
        'content', '').strip() if description_tag else ''
    
    return status_code, h1, title, description 