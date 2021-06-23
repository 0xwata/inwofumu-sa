from numpy import nan
import pandas as pd
import spacy
from spacy.symbols import ADJ, NOUN, PROPN, PRON, VERB
import numpy as np

# 参考 https://yu-nix.com/blog/2021/3/3/spacy-pos-list/
convert_dic = {
    'ADJ': "adjective",
    'NOUN': "noun",
    'PROPN': "noun",
    'PRON': "noun",
    'VERB': "verb",

}
spacy_symbol_noun_list = [NOUN, PROPN, PRON]
df = pd.read_csv("../output/final/3447.csv", sep=',')

nlp = spacy.load("en_core_web_sm")


word_pos_list = []
for i, row in df.iterrows():
    pos_spcy = "other"
    print(row.word_en)
    print(type(row.word_en))
    if row.word_en is np.nan:
        word_pos_list.append("nan")
        continue
    doc = nlp(row.word_en)
    for tok in doc:
        print(tok.text)
        if tok.pos == ADJ:
            pos_spcy = "adjective"
        elif tok.pos == VERB:
            pos_spcy == "verb"
        elif tok.pos in spacy_symbol_noun_list:
            pos_spcy = "noun"
        
        print(pos_spcy, row.word_pos)
        pos_spcy = tok.pos

    word_pos_list.append(pos_spcy)

output_column = ["word", "word_lang", "word_pos", "word_pos_spacy", "word_ipa", "word_ipa_edited_vowel", "word_en", "next_word_index_verb", "next_word_index_noun", "next_word_index_adjective"]

df["word_pos_spacy"] = word_pos_list

df[output_column]
df.to_csv(f'../output/final/{len(df)}_spacy.csv')
print(f"finish writing output to csv")