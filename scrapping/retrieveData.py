import mysql.connector
from scrapping.data import ScrappedReview, EcoReview, Company, Restaurant

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

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    # Example usage:
    retriever = DataConnector()
    data = retriever.retrieve_review_from_mysql("trustPilot")
    
    for row in data:
        print(row.comment)

    retriever.close_connection()
