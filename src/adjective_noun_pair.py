import random
import sentiment_polarity


class AdjectiveNounPairSelector:
    def __init__(self, word_sentiment: str):
        # "positive" or "negative"
        self.word_sentiment = word_sentiment
        # import adjectives list
        with open("EnglishList/english-adjectives.txt") as f:
            self.adjectives = f.readlines()
        # import nouns list
        with open("EnglishList/english-nouns.txt") as f:
            self.nouns = f.readlines()

    def fetch_random_adjective(self) -> str:
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

    def fetch_random_noun(self) -> str:
        noun_index = random.randrange(len(self.nouns))
        return self.nouns[noun_index]

    def __fetch_sentiment_polarity_score(self, word: str) -> float:
        return sentiment_polarity.SentimentPolarity.fetch_score(word)
