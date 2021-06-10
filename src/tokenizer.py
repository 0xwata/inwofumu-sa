import nltk

"""
品詞はこちらで確認できる
https://qiita.com/m__k/items/ffd3b7774f2fde1083fa#%E5%93%81%E8%A9%9E%E3%81%AE%E5%8F%96%E5%BE%97
"""

class Tokenizer():
    def is_target_pos(self, word, target_pos):
        morph = nltk.word_tokenize(word)
        pos = nltk.pos_tag(morph)
        flg = False
        if(pos == target_pos):
            flg = True
        return flg
