from eco_category import EcoCategorizer
from sentiment import SentimentClassifier
from translation import EnFrTranslator
from langdetect import detect
from tqdm import tqdm
import json

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapping.data import ScrappedReview, EcoReview
from scrapping.retrieveData import DataConnector

class ReviewAnalyzer:
    def __init__(self):
        self.translator = EnFrTranslator()
        self.eco_categorizer = EcoCategorizer()
        self.sentiment_classifier = SentimentClassifier()

    def analyze_review(self, review : str) -> tuple[str, str]:
        # Translate review to English if not already in English
        
        if len(review)>10 and len(review)<2000 and detect(review) != "en":
            english_review = self.translator.translate(review)
        else :
            english_review = review

        # Categorize review
        try:
            return self.eco_categorizer.classify_review(english_review), english_review
        except:
            return "other topics", english_review
    
    def eco_review(self, scrap_review : ScrappedReview) -> list[EcoReview]:
        review = scrap_review.comment
        eco_category, english_review = self.analyze_review(review)

        eco_review_list = []

        if eco_category != "other topics":
            # Split review into sentences
            sentences = english_review.split(". ")
            or_sentences = review.split(". ")
            # Categorize each sentence
            for i, sentence in enumerate(sentences):
                try :
                    category, conf= self.eco_categorizer.categorize_review(sentence)
                except :
                    category, _ = "other topics", 0

                if category != "other topics" and conf > 0.5:

                    # Add to list
                    if i < len(or_sentences):
                        sentence = or_sentences[i]
                    # Classify sentiment of sentence
                    sentiment = self.sentiment_classifier.classify_sentiment(sentence)
                    # Calculate rating
                    match sentiment[0]:
                        case "positive":
                            rating = 5
                        case "neutral":
                            rating = 3
                        case _:
                            rating = 1
                    
                    if sentiment[1] < 0.8:
                        rating = scrap_review.rating
                    
                    eco_review_list.append(EcoReview(userName=scrap_review.userName, 
                                                     category=category, rating=rating, 
                                                     comment=sentence, date=scrap_review.date, 
                                                     source=scrap_review.source, 
                                                     company=scrap_review.company,
                                                     restaurant=scrap_review.restaurant))
        # Merge sentences of the same category
        for i, eco_review in enumerate(eco_review_list):
            for j, eco_review2 in enumerate(eco_review_list):
                if i != j and eco_review.category == eco_review2.category:
                    eco_review.comment += ". " + eco_review2.comment
                    eco_review_list.remove(eco_review2)
        return eco_review_list

if __name__ == "__main__":
    # Example usage:
    analyzer = ReviewAnalyzer()
    connector = DataConnector()

    # Retrieve companies and restaurants from MySQL
    companies, restaurants = connector.retrieve_comp_rest_from_mysql()

    # Store the companies and restaurants in a json file
    with open('companies.json', 'w') as fp:
        companies = [company.model_dump() for company in companies]
        dict = {"companies": companies}
        json.dump(dict, fp, ensure_ascii=False, indent=4)
    with open('restaurants.json', 'w') as fp:
        restaurants = [restaurant.model_dump() for restaurant in restaurants]
        dict = {"restaurants": restaurants}
        json.dump(dict, fp, ensure_ascii=False, indent=4)

    data = connector.retrieve_review_from_mysql("google")
    dict = {"eco_reviews": []}
    data = data[0:500]
    for row in tqdm(data):
        eco_review_list = analyzer.eco_review(row)
        for eco_review in eco_review_list:
            dict["eco_reviews"].append(eco_review.model_dump())
            print("--------------------")
            print(eco_review)
            print("--------------------")
    
    # Save the eco_review in a json file
    with open('ecoreviews2.json', 'w') as fp:  
        json.dump(dict, fp, ensure_ascii=False, indent=4)         

    data = connector.retrieve_review_from_mysql("trustPilot")
    
    # Set the columns of the dataframe to the attributes of the EcoReview class
    for row in tqdm(data):
        eco_review_list = analyzer.eco_review(row)
        for eco_review in eco_review_list:
            dict["eco_reviews"].append(eco_review.model_dump())
            print("--------------------")
            print(eco_review)
            print("--------------------")
    
    # Save the eco_review in a json file
    with open('ecoreviews2.json', 'w') as fp:
        json.dump(dict, fp, ensure_ascii=False, indent=4)
            

    
    connector.close_connection()
    