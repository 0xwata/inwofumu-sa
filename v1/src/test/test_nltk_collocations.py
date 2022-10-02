import nltk
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()

# Ngrams with 'creature' as a member
creature_filter = lambda *w: 'kids' not in w
## Bigrams
finder = BigramCollocationFinder.from_words(filtered_sentences)
# only bigrams that appear 3+ times
finder.apply_freq_filter(3)
# only bigrams that contain 'creature'
finder.apply_ngram_filter(creature_filter)
# return the 10 n-grams with the highest PMI
# print (finder.nbest(bigram_measures.likelihood_ratio, 10))
for i in finder.score_ngrams(bigram_measures.likelihood_ratio):
    print (i)
