import nltk
import re

from src.part_of_speech import PartOfSpeech


def find_part_of_speech(word_en: str, lang: str) -> PartOfSpeech:
    morph = nltk.word_tokenize(word_en)
    pos = nltk.pos_tag(morph)
    pos_tag = pos[0][1]
    if re.search('JJ*', pos_tag):
        return PartOfSpeech.adj
    elif re.search('NN*', pos_tag):
        return PartOfSpeech.noun
    elif re.search('VB*', pos_tag):
        return PartOfSpeech.verb
    elif re.search('RB*', pos_tag):
        return PartOfSpeech.adv
    else:
        return PartOfSpeech.other
