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
from scrapping.retrieveData import DataRetriever

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
    
    def eco_review(self, scrap_review : ScrappedReview) -> EcoReview:
        review = scrap_review.comment
        eco_category, english_review = self.analyze_review(review)

        if eco_category != "other topics":
            try :
                category, conf = self.eco_categorizer.categorize_review(english_review)
            except :
                category, conf = "other topics", 0

            if category != "other topics" and conf > 0.4:
                # Classify sentiment of sentence
                try :
                    sentiment = self.sentiment_classifier.classify_sentiment(review)
                except :
                    sentiment = "neutral", 0.5
                # Calculate rating
                match sentiment[0]:
                    case "positive":
                        rating = 5
                    case "neutral":
                        rating = 3
                    case _:
                        rating = 1

                return EcoReview(userName=scrap_review.userName, 
                        category=category, rating=rating, 
                        comment=review, date=scrap_review.date, 
                        source=scrap_review.source, 
                        restaurantName=scrap_review.restaurantName)
            else :
                return None

if __name__ == "__main__":
    # Example usage:
    analyzer = ReviewAnalyzer()
    retriever = DataRetriever()

    data = retriever.retrieve_data_from_mysql("trustPilot")

    dict = {"eco_reviews": []}
    # Set the columns of the dataframe to the attributes of the EcoReview class
    for row in tqdm(data):
        
        eco_review = analyzer.eco_review(row)
        if eco_review is not None:
            dict["eco_reviews"].append(eco_review.model_dump())
            print("--------------------")
            print(eco_review)
            print("--------------------")
    
    retriever.close_connection()

    # Save the dict in a json file
    with open('ecoreviews.json', 'w') as fp:
        json.dump(dict, fp, ensure_ascii=False, indent=4)
    