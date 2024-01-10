from eco_category import EcoCategorizer
from sentiment import SentimentClassifier
from translation import EnFrTranslator
from langdetect import detect

class ReviewAnalyzer:
    def __init__(self):
        self.translator = EnFrTranslator()
        self.eco_categorizer = EcoCategorizer()
        self.sentiment_classifier = SentimentClassifier()

    def analyze_review(self, review):
        # Translate review to English if not already in English
        if detect(review) != "en":
            english_review = self.translator.translate(review)
        else :
            english_review = review

        # Categorize review
        eco_category, conf = self.eco_categorizer.classify_review(english_review)

        # Classify sentiment if eco category is not "other topics"
        if eco_category != "other topics" and conf > 0.5:
            sentiment = self.sentiment_classifier.classify_sentiment(english_review)
            if sentiment[1] < 0.5:
                sentiment = "neutral"
        else:
            sentiment = None

        return eco_category, sentiment

if __name__ == "__main__":
    # Example usage
    review = "Super busy after midnight on New Year's. Staff did great job managing the crowd, and the food was hot and up to standard. That said, they had no time to clean ... garbage cans were overflowing. Then, a minor fight broke out between drunk revellers. I'm sure the atmosphere is much better on most other days, but hey, that's New York on New Year's."
    analyzer = ReviewAnalyzer()
    eco_category, sentiment = analyzer.analyze_review(review)
    print(f"Eco category: {eco_category}")
    print(f"Sentiment: {sentiment}")
    