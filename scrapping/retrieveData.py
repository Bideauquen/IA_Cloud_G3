import mysql.connector

def retrieve_trustpilot_data_from_mysql():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3307,
        password="password",
        database="reviews"
    )

    cursor = connection.cursor()

    query = """
        SELECT userName, reviewTitle, rating, comment, date, source, restaurantName
        FROM trustPilot
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

data = retrieve_trustpilot_data_from_mysql()

for row in data:
    print(row)
