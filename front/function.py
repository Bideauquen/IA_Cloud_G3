import requests
import json

def get_lat_long(api_key, address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['status'] == 'OK':
            # Récupérer les coordonnées de latitude et longitude
            location = data['results'][0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            return latitude, longitude
        else:
            print(f"Erreur lors de la géocodification de {address}: {data['status']}")
            return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la géocodification de {address}: {e}")
        return None

def update_coordinates(api_key, restaurants):
    for restaurant in restaurants:
        address = restaurant['address']
        coordinates = get_lat_long(api_key, address)
        print(f"Coordonnées de {address}: {coordinates}")
        # écrire par dessus les anciennes coordonnées dans le fichier
        restaurant['latitude'] = coordinates[0]
        restaurant['longitude']= coordinates[1]
        restaurant['coordinates'] = coordinates
    with open('../restaurants.json', 'w') as file:
        dict = {"restaurants": restaurants}
        json.dump(dict, file, ensure_ascii=False, indent=4)

# Remplacez 'VOTRE_CLE_API' par votre clé API Google Maps
api_key = 'AIzaSyBE6J0FRoS4EJ0AVv6bILp-qzU7q1zHsmo'
def maj_coord():
    # Charger le contenu du fichier JSON dans un dictionnaire
    with open('../restaurants.json', 'r') as file:
        data = json.load(file)

    # Mettre à jour les coordonnées
    update_coordinates(api_key, data["restaurants"])

def maj_rating():
    # Charger les données depuis les fichiers JSON
    with open('static/companies.json', 'r') as companies_file:
        companies_data = json.load(companies_file)

    with open('static/restaurants.json', 'r') as restaurants_file:
        restaurants_data = json.load(restaurants_file)

    # Créer un dictionnaire pour mapper l'id de la company à ses ratings
    company_ratings = {company['id']: company['ratings'] for company in companies_data['companies']}

    # Parcourir les restaurants et ajouter le champ "rating" en fonction de l'id de la company
    for restaurant in restaurants_data:
        company_id = restaurant['company']
        rating = company_ratings.get(company_id, "No rating available")
        restaurant['rating'] = rating.split(', ')  # Séparer les ratings en une liste

    # Enregistrer les modifications dans restaurants.json
    with open('static/restaurants.json', 'w') as restaurants_file:
        json.dump(restaurants_data, restaurants_file, indent=2)

maj_rating()