import requests
import json
import pandas as pd
import os


def scrape_google_reviews(api_key, place_id):
    # URL de l'API Google Places
    api_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,reviews&key={api_key}'

    # Envoi de la requête à l'API
    response = requests.get(api_url)
    data = response.json()
    print(data)

    # Vérification si la requête a réussi
    if response.status_code == 200:
        # Initialisation des listes pour stocker les données des avis
        review_texts = []
        review_ratings = []

        # Extraction des données des avis
        reviews = data.get('result', {}).get('reviews', [])
        for review in reviews:
            review_texts.append(review.get('text', ''))
            review_ratings.append(review.get('rating', ''))

        # Création d'un dataframe à partir des données des avis
        df = pd.DataFrame({'Review': review_texts, 'Rating': review_ratings})

        return df
    else:
        print(f"Erreur lors de la requête à l'API Google Places: {response.status_code}")
        return None

# Remplacez 'YOUR_API_KEY' par votre clé d'API Google Places
api_key = 'AIzaSyDA0LIJnsdC0aN7AymEmBtqLds94gmW1i4'
place_id = '0x89c258f1fcd66869:0x65d72e84d91a3f14'  # Remplacez par l'ID de l'emplacement que vous souhaitez récupérer

df = scrape_google_reviews(api_key, place_id)
if df is not None:
    print(df)
