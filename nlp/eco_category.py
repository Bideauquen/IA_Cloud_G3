from transformers import pipeline

class EcoCategorizer:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v1.1-all-33")
        self.categories = ["organic, pesticide, antibiotics, health", 
                        "climate, vegan, renewable, local", 
                        "waste, plastic, packaging",
                        "social, diversity, ethics",
                        "governance, transparency",
                        "water management, ocean pollution",
                        "greenwashing, lobbying",
                        "other topics"]
        self.classes = ["environment concerns", "other topics"]

        self.hypothesis_template = "This review is about {}"

    def classify_review(self, review):
        output = self.classifier(review, self.classes, hypothesis_template=self.hypothesis_template, multi_label=False)
        return output["labels"][0]

    def categorize_review(self, review):
        """
        Categorize a list of reviews
        """
        output = self.classifier(review, self.categories, hypothesis_template=self.hypothesis_template, multi_label=False)
        return output["labels"][0].split(", ")[0], output["scores"][0]

if __name__ == "__main__":
    # Example usage
    text = "Super busy after midnight on New Year's. Staff did great job managing the crowd, and the food was hot and up to standard. That said, they had no time to clean ... garbage cans were overflowing. Then, a minor fight broke out between drunk revellers. I'm sure the atmosphere is much better on most other days, but hey, that's New York on New Year's."
    categorizer = EcoCategorizer()
    output = categorizer.classify_review(text)
    print(output)
