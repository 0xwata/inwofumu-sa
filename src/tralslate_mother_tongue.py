import pandas as pd
from translate import Translate
import time
"""
下に表示する言語
・英語
・日本語 ja
・インドネシア語: id
・中国語 zh-cn
"""

translate = Translate()

output_column = ["word", "word_lang", "word_pos", "word_ipa", "word_ipa_edited_vowel", "word_en", "next_word_index_verb", "next_word_index_noun", "next_word_index_adjective", "word_id"]


df = pd.read_csv("../output/final/final/output_after_screaning.csv", sep=',', index_col=0)
print(df.columns)
df_word = df.word
df_word_en = df.word_en
df_word_lang = df.word_lang
result = []
group_word_id = []
for idx in range(df.shape[0]):
    word = df_word.iloc[idx]
    word_en = df_word_en.iloc[idx]
    word_lang = df_word_lang.iloc[idx]
    if word_lang == "id":
        print(word)
        group_word_id.append(word)
    else:
    	word_id = translate.translate_by_language(word_en, "id")
    	group_word_id.append(word_id)
    	time.sleep(1)
    print("current_idx:" + str(idx) + "/" + str(len(df)))

df["word_id"] = group_word_id
df_blank = df[df["word_id"] == ""]
print(len(df_blank))
df[output_column]

df.to_csv(f'../output/final/final/output_after_screaning_v3.csv')

