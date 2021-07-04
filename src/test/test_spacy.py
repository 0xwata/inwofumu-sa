from numpy import nan
import pandas as pd
import spacy
from spacy.symbols import ADJ, NOUN, PROPN, PRON, VERB
import numpy as np

spacy_symbol_noun_list = [NOUN, PROPN, PRON]

nlp_en = spacy.load("en_core_web_sm")
nlp_zh = spacy.load("zh_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")
nlp_de = spacy.load("de_core_news_sm")
nlp_ja = spacy.load("ja_core_news_sm")
nlp_ro = spacy.load("ro_core_news_sm")

lang_converter_dic_for_spacy = {
    "de":nlp_de,#
    "en":nlp_en,#
    "es":nlp_es,#
    "ja":nlp_ja,#
    "ro":nlp_ro,#
    "zh-cn":nlp_zh,#
    # "eo":"eo",
    # "id":nlp_id,
    # "ko":nlp_ko,
}

df = pd.read_csv("../output/final/3447.csv", sep=',', index_col=0)

print(ADJ, NOUN, PROPN, PRON, VERB)
word_pos_list = []
for i, row in df.iterrows():
    pos_spcy = "other"

    if row.word_lang in lang_converter_dic_for_spacy.keys():
        nlp = lang_converter_dic_for_spacy[row.word_lang]
        if row.word is np.nan:
            word_pos_list.append("nan")
            continue
        target_word = row.word
    else:
        nlp = nlp_en
        if row.word_en is np.nan:
            word_pos_list.append("nan")
            continue
        target_word = row.word_en

    doc = nlp(target_word)
    for tok in doc:
        print(tok.text)
        if tok.pos == ADJ:
            pos_spcy = "adjective"
        elif tok.pos == VERB:
            pos_spcy = "verb"
        elif tok.pos in spacy_symbol_noun_list:
            pos_spcy = "noun"

        print(tok.pos, pos_spcy, row.word_pos)

    print("append", pos_spcy)
    word_pos_list.append(pos_spcy)

output_column = ["word", "word_lang", "word_pos", "word_pos_spacy", "word_ipa", "word_ipa_edited_vowel", "word_en", "next_word_index_verb", "next_word_index_noun", "next_word_index_adjective"]

df["word_pos_spacy"] = word_pos_list

df_output = df[output_column]
df_output.to_csv(f'../output/final/{len(df_output)}_spacy.csv')
print(f"finish writing output to csv")