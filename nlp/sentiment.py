from transformers import pipeline

distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    return_all_scores=True
)

# english
response = distilled_student_sentiment_classifier ("L’ambiance est très agréable et le restaurant est propre. L’équipe rapide et souriante. Merci pour Alexandra de son accueil et aide sur le menu ☺️")
print(response)