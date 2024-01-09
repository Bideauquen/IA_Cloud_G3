from transformers import pipeline

text = "Angela Merkel est une femme politique allemande et leader du parti conservateur CDU."
hypothesis_template = "Cette phrase porte sur {}"
classes_verbalized = ["la politique", "l'economy", "le divertissement", "l'environnement"]
zeroshot_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v1.1-all-33")
output = zeroshot_classifier(text, classes_verbalized, hypothesis_template=hypothesis_template, multi_label=False)
print(output)