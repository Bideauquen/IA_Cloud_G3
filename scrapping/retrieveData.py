import mysql.connector
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapping.data import ScrappedReview, EcoReview, Company, Restaurant
import json

class DataConnector:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3307,
            password="password",
            database="reviews"
        )

    def retrieve_review_from_mysql(self, table: str) -> list[ScrappedReview]:
    
        cursor = self.connection.cursor()

        if table == "trustPilot":
            i = 0
            columns = ["userName", "rating", "reviewTitle", "comment", "date", "company"]
        else :
            i = 1
            columns = ["userName", "rating", "comment", "date", "restaurant"] # Google Reviews

        query = f"""
            SELECT {', '.join(columns)}
            FROM {table}
        """

        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        # Convert to list of ScrappedReview objects
        result = [ScrappedReview(userName=row[0], 
                                 rating=row[1],
                                 reviewTitle=row[2] if table == "trustPilot" else "", 
                                 comment=row[3-i] if row[3-i] is not None else "", 
                                 date=row[4-i] if row[4-i] is not None else "", 
                                 source=table,
                                 company=row[5-i] if table == "trustPilot" else -1,
                                 restaurant=row[5-i] if table == "google" else -1) for row in result]

        return result

    def retrieve_comp_rest_from_mysql(self) -> tuple[list[Company], list[Restaurant]]:
        cursor = self.connection.cursor()

        query_comp = """
            SELECT id, name, ecoScore, ratings, reviewCount
            FROM companies
        """
        query_rest = """
            SELECT id, name, company, address, longitude, latitude, ecoScore, ratings, reviewCount
            FROM restaurants
        """

        cursor.execute(query_comp)
        result_comp = cursor.fetchall()
        result_comp = [Company(id=row[0], name=row[1], ecoScore=row[2] if row[2] is not None else -1,
                                ratings=row[3] if row[3] is not None else "", reviewCount=row[4]) for row in result_comp]

        cursor.execute(query_rest)
        result_rest = cursor.fetchall() 
        result_rest = [Restaurant(id=row[0], name=row[1], company=row[2], 
                                  address=row[3], longitude=row[4] if row[4] is not None else -1, 
                                  latitude=row[5] if row[5] is not None else -1,
                                  ecoScore=row[6] if row[6] is not None else -1, 
                                  ratings=row[7] if row[7] is not None else "", 
                                  reviewCount=row[8] if row[8] is not None else 0) for row in result_rest]
        cursor.close()

        return result_comp, result_rest

    def push_company_into_mysql(self, company: Company):
        cursor = self.connection.cursor()

        query = """
            INSERT INTO companies (name, ecoScore, ratings, reviewCount)
            VALUES (%s, %s, %s, %s)
        """

        data = (company.name,
                company.ecoScore,
                company.ratings,
                company.reviewCount)

        cursor.execute(query, data)
        self.connection.commit()
        cursor.close()
    
    def push_restaurant_into_mysql(self, restaurant: Restaurant):
        cursor = self.connection.cursor()

        query = """
            INSERT INTO restaurants (name, company, address, longitude, latitude, ecoScore, ratings, reviewCount)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (restaurant.name,
                restaurant.company,
                restaurant.address,
                restaurant.longitude,
                restaurant.latitude,
                restaurant.ecoScore,
                restaurant.ratings,
                restaurant.reviewCount)

        cursor.execute(query, data)
        self.connection.commit()
        cursor.close()
    
    def push_eco_review_into_mysql(self, eco_review: EcoReview):
        cursor = self.connection.cursor()

        query = """
            INSERT INTO ecoreviews (userName, category, rating, comment, date, source, company, restaurant)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (eco_review.userName,
                eco_review.category,
                eco_review.rating,
                eco_review.comment,
                eco_review.date,
                eco_review.source,
                eco_review.company,
                eco_review.restaurant)

        cursor.execute(query, data)
        self.connection.commit()
        cursor.close()

    def score_company_in_mysql(self, company: Company):
        cursor = self.connection.cursor()

        # Find all the ecoreviews with the company id
        query = """
            SELECT rating, category
            FROM ecoreviews
            WHERE company = %s
        """

        print(company.id)

        cursor.execute(query, (company.id,))
        result = cursor.fetchall()
        cursor.close()

        ratings = [0 for i in range(3)]
        ratings_count = [0 for i in range(3)]

        # Compute the ratings for each category
        for rating, category in result:
            match category:
                case "climate" | "waste" | "water":
                    ratings[0] += rating
                    ratings_count[0] += 1
                case "organic":
                    ratings[1] += rating
                    ratings_count[1] += 1
                case "governance" | "social" | "greenwashing":
                    ratings[2] += rating
                    ratings_count[2] += 1
        
        # Compute the average rating for each category
        for i in range(3):
            if ratings_count[i] != 0:
                ratings[i] /= ratings_count[i]
            else:
                ratings[i] = None
        
        # Compute the ecoScore
        ecoScore = 0
        for rating in ratings:
            if rating is not None:
                ecoScore += rating
        
        # Update the company in the database
        cursor = self.connection.cursor()
        query = """
            UPDATE companies
            SET ecoScore = %s, ratings = %s, reviewCount = %s
            WHERE id = %s
        """
        data = (ecoScore,
                ", ".join([str(rating) for rating in ratings]),
                sum(ratings_count),
                company.id)
        cursor.execute(query, data)
        self.connection.commit()
        cursor.close()
    
    def score_restaurant_in_mysql(self, restaurant: Restaurant):
        cursor = self.connection.cursor()

        # Find all the ecoreviews with the restaurant id
        query = """
            SELECT rating, category
            FROM ecoreviews
            WHERE restaurant = %s
        """

        cursor.execute(query, (restaurant.id,))
        result = cursor.fetchall()
        cursor.close()

        ratings = [0 for i in range(3)]
        ratings_count = [0 for i in range(3)]

        # Compute the ratings for each category
        for rating, category in result:
            match category:
                case "climate" | "waste" | "water":
                    ratings[0] += rating
                    ratings_count[0] += 1
                case "organic":
                    ratings[1] += rating
                    ratings_count[1] += 1
                case "governance" | "social" | "greenwashing":
                    ratings[2] += rating
                    ratings_count[2] += 1
        
        # Compute the average rating for each category
        for i in range(3):
            if ratings_count[i] != 0:
                ratings[i] /= ratings_count[i]
            else:
                ratings[i] = None
        
        # Compute the ecoScore
        ecoScore = 0
        for rating in ratings:
            if rating is not None:
                ecoScore += rating
        
        # Update the company in the database
        cursor = self.connection.cursor()
        query = """
            UPDATE restaurants
            SET ecoScore = %s, ratings = %s, reviewCount = %s
            WHERE id = %s
        """
        data = (ecoScore,
                ", ".join([str(rating) for rating in ratings]),
                sum(ratings_count),
                restaurant.id)
        cursor.execute(query, data)
        self.connection.commit()
        cursor.close()
        
    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    # Example usage:
    retriever = DataConnector()
    
    # Update the scores of the companies
    companies, restaurants = retriever.retrieve_comp_rest_from_mysql()
    for company in companies:
        retriever.score_company_in_mysql(company)
    for restaurant in restaurants:
        retriever.score_restaurant_in_mysql(restaurant)
    
    # Retrieve companies and restaurants from MySQL
    companies, restaurants = retriever.retrieve_comp_rest_from_mysql()

    # Store the companies and restaurants in a json file
    with open('companies.json', 'w') as fp:
        companies = [company.model_dump() for company in companies]
        dict = {"companies": companies}
        json.dump(dict, fp, ensure_ascii=False, indent=4)
    with open('restaurants.json', 'w') as fp:
        restaurants = [restaurant.model_dump() for restaurant in restaurants]
        dict = {"restaurants": restaurants}
        json.dump(dict, fp, ensure_ascii=False, indent=4)

    retriever.close_connection()
