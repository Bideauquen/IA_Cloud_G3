import requests

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
            print(f"Erreur: {data['status']}")
            return None
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None

# Remplacez 'VOTRE_CLE_API' par votre clé API Google Maps
api_key = 'AIzaSyBE6J0FRoS4EJ0AVv6bILp-qzU7q1zHsmo'
adresse = '10B rue Pilar, 64000 Pau'

coordinates = get_lat_long(api_key, adresse)
print(coordinates)