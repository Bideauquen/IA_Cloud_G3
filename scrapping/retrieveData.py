import mysql.connector
from scrapping.data import ScrappedReview

class DataConnector:
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

        if table == "trustPilot":
            columns = ["userName", "rating", "reviewTitle", "comment", "date", "source", "company"]
        else :
            columns = ["userName", "rating", "reviewTitle", "comment", "date", "source", "restaurant"] # Google Reviews

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
                                 reviewTitle=row[2], 
                                 comment=row[3] if row[3] is not None else "", 
                                 date=row[4], 
                                 source=table,
                                 company=row[6] if table == "trustPilot" else -1,
                                 restaurant=row[6] if table == "google" else -1) for row in result]

        return result

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    # Example usage:
    retriever = DataConnector()
    data = retriever.retrieve_data_from_mysql("trustPilot")
    
    for row in data:
        print(row.comment)

    retriever.close_connection()
