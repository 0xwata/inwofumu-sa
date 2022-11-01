import nltk
import re
from numpy import nan
import pandas as pd
import spacy
from spacy.symbols import ADJ, NOUN, PROPN, PRON, VERB
import numpy as np

"""
品詞はこちらで確認できる
https://qiita.com/m__k/items/ffd3b7774f2fde1083fa#%E5%93%81%E8%A9%9E%E3%81%AE%E5%8F%96%E5%BE%97
"""


# target_pos_li = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBN", "VBP", "VBZ"]

class Tokenizer:

    def fetch_target_pos(self, word: str) -> str:
        morph = nltk.word_tokenize(word)
        pos = nltk.pos_tag(morph)
        pos_tag = pos[0][1]
        print(pos_tag)
        print()
        if re.search('JJ', pos_tag):
            return "adjective"
        elif re.search('NN', pos_tag):
            return "noun"
        elif re.search('VB', pos_tag):
            return "verb"
        return ""


class TokenizerSpacy:
    def __init__(self):
        self.spacy_symbol_noun_list = [NOUN, PROPN, PRON]

        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_zh = spacy.load("zh_core_web_sm")
        self.nlp_es = spacy.load("es_core_news_sm")
        self.nlp_de = spacy.load("de_core_news_sm")
        self.nlp_ja = spacy.load("ja_core_news_sm")
        self.nlp_ro = spacy.load("ro_core_news_sm")

        self.lang_converter_dic_for_spacy = {
            "de": self.nlp_de,  #
            "en": self.nlp_en,  #
            "es": self.nlp_es,  #
            "ja": self.nlp_ja,  #
            "ro": self.nlp_ro,  #
            "zh-cn": self.nlp_zh,  #
            # "eo":"eo",
            # "id":nlp_id,
            # "ko":nlp_ko,
        }

    def fetch_target_pos(self, word:str, word_en:str, lang:str) -> str:
        if lang in self.lang_converter_dic_for_spacy.keys():
            nlp = self.lang_converter_dic_for_spacy[lang]
            if word is np.nan:
                return ""
            target_word = word
        else:
            nlp = self.nlp_en
            if word_en is np.nan:
                return ""
            target_word = word_en
        doc = nlp(target_word)
        pos_spcy = ""
        for tok in doc:
            if tok.pos == ADJ:
                pos_spcy = "adjective"
            elif tok.pos == VERB:
                pos_spcy = "verb"
            elif tok.pos in self.spacy_symbol_noun_list:
                pos_spcy = "noun"
        return pos_spcy