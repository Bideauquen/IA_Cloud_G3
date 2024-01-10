import mysql.connector

class DataRetriever:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3307,
            password="password",
            database="reviews"
        )

    def retrieve_trustpilot_data_from_mysql(self):
        cursor = self.connection.cursor()

        query = """
            SELECT userName, reviewTitle, rating, comment, date, source, restaurantName
            FROM trustPilot
        """

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()

        return result

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    # Example usage:
    retriever = DataRetriever()
    data = retriever.retrieve_trustpilot_data_from_mysql()

    for row in data:
        print(row)

    retriever.close_connection()
