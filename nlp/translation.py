from transformers import pipeline
from transformers import pipeline

class EnFrTranslator:
    def __init__(self):
        self.translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

    def translate(self, text):
        translated = self.translator(text)
        return translated[0]['translation_text']

if __name__ == "__main__":
    translator = EnFrTranslator()
    text = "The weather is beautiful today."
    translated_text = translator.translate(text)
    print(f"Translated text: {translated_text}")
