import requests
from bs4 import BeautifulSoup
import mysql.connector

class TrustPilotScrapper:
    def __init__(self, company_url, company_name):
        self.company_url = company_url
        self.company_name = company_name
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3307,
            password="password",
            database="reviews"
        )

    def extract_review_details(self, review):
        reviewData = {}

        # Extract the user name
        userName = review.find('span', class_='typography_heading-xxs__QKBS8')
        reviewData['userName'] = userName.get_text(strip=True) if userName else None

        # Extract the review title
        reviewTitle = review.find('h2', class_='typography_heading-s__f7029')
        reviewData['reviewTitle'] = reviewTitle.get_text(strip=True) if reviewTitle else None

        # Extract the rating
        rating = review.find('div', class_='star-rating_starRating__4rrcf')
        reviewData['rating'] = int(rating.img['alt'][5]) if rating and rating.img['alt'][5].isdigit() else None

        # Extract the comment
        comment = review.find('p', class_='typography_body-l__KUYFJ')
        reviewData['comment'] = comment.get_text(strip=True) if comment else None

        # Extract the date of the experience
        date = review.find('p', class_='typography_body-m__xgxZ_')
        reviewData['date'] = date.get_text(strip=True) if date else None

        return reviewData

    def parse_html(self, html):
        if html is None:
            return []

        try:
            soup = BeautifulSoup(str(html), 'html.parser')
            articles = soup.find_all('article', class_='paper_paper__1PY90')

            reviews = []
            for article in articles:
                review = self.extract_review_details(article)
                reviews.append(review)

            return reviews
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def insert_company_into_mysql(self, company_name):
        cursor = self.connection.cursor()

        # Test if the company already exists in the database
        query = "SELECT id FROM companies WHERE name = %s"
        cursor.execute(query, (company_name,))
        result = cursor.fetchone()
        
        if result is None:
            query = """
                INSERT INTO companies (name, ecoScore, ratings, reviewCount)
                VALUES (%s, %s, %s, %s)
            """

            data = (company_name,
                    None,
                    None,
                    0)

            cursor.execute(query, data)

            # Get the company id
            company_id = cursor.lastrowid
            self.connection.commit()
            cursor.close()
        else:
            company_id = result[0]
        return company_id


    def insert_review_into_mysql(self, review, company_id):

        cursor = self.connection.cursor()

        query = """
            INSERT INTO trustPilot (userName, rating, reviewTitle, comment, date, company)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        data = (
            review['userName'],
            review['rating'],
            review['reviewTitle'],
            review['comment'],
            review['date'],
            company_id,
        )

        cursor.execute(query, data)
        self.connection.commit()
        cursor.close()

    def scrape_company(self):
        response = requests.get(self.company_url)
        i = 2
        all_reviews_soup = []
        while response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            reviews_soup = soup.find_all('article', attrs={'class':"paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_reviewCard__hcAvl"})
            all_reviews_soup.append(reviews_soup)
            response = requests.get(f'{self.company_url}?page={i}')
            i += 1
        i -= 1

        # Insert the company into the companies table
        company_id = self.insert_company_into_mysql(self.company_name)

        for page_idx, html_article_list in enumerate(all_reviews_soup, 1):
            for html_article in html_article_list:
                if html_article is not None:
                    reviews = self.parse_html(html_article)
                    
                    # Insert the reviews into the reviews table
                    for review in reviews:
                        self.insert_review_into_mysql(review, company_id)
        
        self.connection.close()

if __name__ == "__main__":
    companies = [
        ('https://fr.trustpilot.com/review/www.hippopotamus.fr', 'Hippopotamus France'),
        ('https://fr.trustpilot.com/review/mcdonalds.fr', 'Mcdonalds France'),
        ('https://fr.trustpilot.com/review/buffalo-grill.fr', 'Buffalo Grill'),
        ('https://fr.trustpilot.com/review/flunch.fr', 'Flunch'),
        ('https://fr.trustpilot.com/review/ayakosushi.fr', 'Ayako Sushi'),
        ('https://fr.trustpilot.com/review/sushishop.fr', 'Sushi Shop'),
        ('https://fr.trustpilot.com/review/subway.com', 'Subway'),
        ('https://fr.trustpilot.com/review/kfc.fr', 'KFC France')
    ]

    for company_url, company_name in companies:
        scrapper = TrustPilotScrapper(company_url, company_name)
        scrapper.scrape_company()
