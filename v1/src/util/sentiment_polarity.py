from textblob import TextBlob


class SentimentPolarity():
    def __init__(self):
        pass

    @staticmethod
    def fetch_score(word: str) -> float:
        return TextBlob(word).sentiment
