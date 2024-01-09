import requests
from bs4 import BeautifulSoup


def scraping():
    response = requests.get('https://fr.trustpilot.com/review/mcdonalds.fr')
    i = 2
    all_avis_soup = []
    while response.status_code == 200 :
        soup = BeautifulSoup(response.content, "html.parser")

        avis_soup = soup.find_all('article', attrs={'class':"paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_reviewCard__hcAvl"})
        all_avis_soup.append(avis_soup)
        response = requests.get(f'https://fr.trustpilot.com/review/mcdonalds.fr?page={i}')
        i = i+1
    i=i-1
    return all_avis_soup, i

avis, pages = scraping()
print("PAGES", pages)
print("Avis page 3", [text.p.text for text in avis[2]])