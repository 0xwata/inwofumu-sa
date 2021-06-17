import nltk
import re
"""
品詞はこちらで確認できる
https://qiita.com/m__k/items/ffd3b7774f2fde1083fa#%E5%93%81%E8%A9%9E%E3%81%AE%E5%8F%96%E5%BE%97
"""

# target_pos_li = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBN", "VBP", "VBZ"]

class Tokenizer():
    def fetch_target_pos(self, word) -> str:
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