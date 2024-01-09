from transformers import pipeline

class SentimentClassifier:
    def __init__(self):
        self.distilled_student_sentiment_classifier = pipeline(
            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
            top_k=1,
        )
    
    def classify_sentiment(self, review):
        response = self.distilled_student_sentiment_classifier(review)[0]
        return response[0]["label"], response[0]["score"]

if __name__ == "__main__":
    classifier = SentimentClassifier()
    review = "L’ambiance est très agréable et le restaurant est propre. L’équipe rapide et souriante. Merci pour Alexandra de son accueil et aide sur le menu ☺️"
    response = classifier.classify_sentiment(review)
    print(response)