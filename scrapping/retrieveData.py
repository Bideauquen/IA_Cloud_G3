import mysql.connector
from scrapping.data import ScrappedReview

class DataRetriever:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3307,
            password="password",
            database="reviews"
        )

    def retrieve_data_from_mysql(self, table: str) -> list[ScrappedReview]:
    
        cursor = self.connection.cursor()

        query = f"""
            SELECT userName, reviewTitle, rating, comment, date, source, restaurantName
            FROM {table}
        """

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()

        # Convert to list of ScrappedReview objects
        result = [ScrappedReview(userName=row[0], reviewTitle=row[1], rating=row[2], comment=row[3] if row[3] is not None else "", date=row[4], source=row[5], restaurantName=row[6]) for row in result]

        return result

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    # Example usage:
    retriever = DataRetriever()
    data = retriever.retrieve_data_from_mysql("trustPilot")
    
    for row in data:
        print(row.comment)

    retriever.close_connection()
