from google_maps_reviews import ReviewsClient

client = ReviewsClient(api_key='AIzaSyCxKV826MRMp1NQnGdZiuXEKmvHw8Oa45g')

# Get reviews from the place by name and lcoation
results = client.get_reviews('Trump Tower, NY, USA', language='en')

print(results)