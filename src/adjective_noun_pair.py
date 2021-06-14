import random
import sentiment_polarity

BASE_URL = "../data/random-adjectives-nouns/"


class AdjectiveNounPairSelector:
    def __init__(self):
        # "positive" or "negative"
        # self.word_sentiment = word_sentiment

        # import adjectives list
        with open(BASE_URL + "english-adjectives.txt") as f:
            self.adjectives = f.readlines()
        print("adjectiveリストの読み込み完了")
        # import nouns list
        with open(BASE_URL + "english-nouns.txt") as f:
            self.nouns = f.readlines()
        print("nounリストの読み込み完了")

    def fetch_random_adjective(self) -> str:
        adj_index = random.randrange(len(self.adjectives))
        return self.adjectives[adj_index]

    def fetch_random_noun(self) -> str:
        noun_index = random.randrange(len(self.nouns))
        return self.nouns[noun_index]

    def fetch_random_adjective_with_sentiment(self) -> str:
        sentiment_score = 0
        if self.word_sentiment == "positive":
            sentiment_score_threshold = 0.8
            while sentiment_score < sentiment_score_threshold:
                adj_index = random.randrange(len(self.adjectives))
                sentiment_score = self.fetch_sentiment_polarity_score(self.adjectives[adj_index])
        else:
            sentiment_score_threshold = -0.8
            while sentiment_score > sentiment_score_threshold:
                adj_index = random.randrange(len(self.adjectives))
                sentiment_score = self.fetch_sentiment_polarity_score(
                    self.adjectives[adj_index]
                )
        return self.adjectives[adj_index]

    def fetch_sentiment_polarity_score(self, word: str) -> float:
        return sentiment_polarity.SentimentPolarity.fetch_score(word)
