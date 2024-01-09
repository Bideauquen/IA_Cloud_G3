import requests
from bs4 import BeautifulSoup
import mysql.connector

def extract_review_details(review):
    reviewData = {}

    # Extrait le nom de l'utilisateur
    userName = review.find('span', class_='typography_heading-xxs__QKBS8')
    reviewData['userName'] = userName.get_text(strip=True) if userName else None
    
    # Extrait le titre de la review
    reviewTitle = review.find('h2', class_='typography_heading-s__f7029')
    reviewData['reviewTitle'] = reviewTitle.get_text(strip=True) if reviewTitle else None

    # Extrait la note
    rating = review.find('div', class_='star-rating_starRating__4rrcf')
    reviewData['rating'] = int(rating.img['alt'][5]) if rating and rating.img['alt'][5].isdigit() else None

    # Extrait le commentaire
    comment = review.find('p', class_='typography_body-l__KUYFJ')
    reviewData['comment'] = comment.get_text(strip=True) if comment else None

    # Extrait la date de l'expérience
    date = review.find('p', class_='typography_body-m__xgxZ_')
    reviewData['date'] = date.get_text(strip=True) if date else None

    return reviewData

def parse_html(html):
    if html is None:
        return []
    
    try:
        soup = BeautifulSoup(str(html), 'html.parser')
        articles = soup.find_all('article', class_='paper_paper__1PY90')

        reviews = []
        for article in articles:
            review = extract_review_details(article)
            reviews.append(review)

        return reviews
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def insert_into_mysql(review):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        port = 3307,
        password="password",
        database="reviews"
    )

    cursor = connection.cursor()

    query = """
        INSERT INTO reviews (userName, reviewTitle, rating, comment, date, source, restaurantName)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    data = (
        review['userName'],
        review['reviewTitle'],
        review['rating'],
        review['comment'],
        review['date'],
        "TrustPilot",
        "McDonaldFr"
    )

    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()
    
    
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
# print("Avis page 3", [text.p.text for text in avis[2]])

for page_idx, html_article_list in enumerate(avis, 1):
    # Itération sur les éléments de la liste html_article_list
    for html_article in html_article_list:
        if html_article is not None:
            reviews = parse_html(html_article)

            # Insére les critiques dans MySQL
            for review in reviews:
                insert_into_mysql(review)
