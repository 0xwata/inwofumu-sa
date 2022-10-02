import pandas as pd
import numpy as np

def fetch_next_index (next_word_index: str):
    if type(next_word_index) == str:
        next_word_indexs = next_word_index.split(":")
    else:
        return None
    return next_word_indexs


df = pd.read_csv("../output/final/final/output_after_screaning_v4_ja_screaning_next_search_index_screaning.csv", sep=",", index_col=0)

print(df.columns)

df["next_word_index_verb_count"] = df["next_word_index_verb"].apply(lambda x: len(x.split(":")) if type(x) == str else 0)
df["next_word_index_adjective_count"] = df["next_word_index_adjective"].apply(lambda x: len(x.split(":")) if type(x) == str else 0)
df["next_word_index_noun_count"] = df["next_word_index_noun"].apply(lambda x: len(x.split(":")) if type(x) == str else 0)

df_verb_adjective_ok = df[(df["next_word_index_verb_count"] >= 3) & (df["next_word_index_adjective_count"] >= 3)]
df_verb_noun_ok = df[(df["next_word_index_verb_count"] >= 3) & (df["next_word_index_noun_count"] >= 3)]
df_noun_adjective_ok = df[(df["next_word_index_noun_count"] >= 3) & (df["next_word_index_adjective_count"] >= 3)]
df_verb_noun_adjective_ok = df[(df["next_word_index_verb_count"] >= 3) & (df["next_word_index_noun_count"] >= 3) & (df["next_word_index_adjective_count"] >= 3)]

output_column = ["word", "word_lang", "word_pos", "word_ipa", "word_ipa_edited_vowel", "word_en", "next_word_index_verb", "next_word_index_noun", "next_word_index_adjective", "word_ch", "word_id","word_ja"]


print(df.groupby("next_word_index_verb_count").size())
print(df.groupby("next_word_index_adjective_count").size())
print(df.groupby("next_word_index_noun_count").size())
print(len(df_verb_adjective_ok))
print(len(df_verb_noun_ok))
print(len(df_noun_adjective_ok))
print(len(df_verb_noun_adjective_ok))
print(len(df))
if len(df) == len(df_verb_noun_adjective_ok):
    print("スクリーニング完了")

df_verb_noun_adjective_ok[output_column].to_csv(f'../output/final/final/output_after_screaning_v4_ja_screaning.csv')
print(df_verb_noun_adjective_ok.groupby("word_pos").size())
print(df_verb_noun_adjective_ok.groupby("word_lang").size())


# """
# ,word,word_lang,word_pos,word_ipa,word_ipa_edited_vowel,word_en,next_word_index_verb,next_word_index_adjective,next_word_index_noun
# """
# for index, row in df.iterrows():
#     next_word_index_verb = row["next_word_index_verb"]
#     next_word_index_verbs = fetch_next_index(next_word_index_verb)
#     if next_word_index_verbs is None:
#         continue

#     next_word_index_noun = row["next_word_index_noun"]
#     next_word_index_nouns = fetch_next_index(next_word_index_noun)
#     if next_word_index_nouns is None:
#         continue

#     next_word_index_adjective = row["next_word_index_adjective"]
#     next_word_index_adjectives = fetch_next_index(next_word_index_adjective)
#     if next_word_index_adjective is None:
#         continue


#     word = row["word"]
#     word_ipa = row["word_ipa"]
#     word_ipa_edited_vowel = row["word_ipa_edited_vowel"]

#     for index in next_word_index_verbs:
#         i = int(index)
#         print(word, word_ipa, word_ipa_edited_vowel)

#         index_word = df[i:i+1]["word"].values[0]
#         index_word_ipa = df[i:i+1]["word_ipa"].values[0]
#         index_word_ipa_edited_vowel = df[i:i+1]["word_ipa_edited_vowel"].values[0]

#         print(index_word, index_word_ipa, index_word_ipa_edited_vowel)
#         print()

#         next_word_index_verb = row["next_word_index_verb"]
#         next_word_index_verbs = fetch_next_index(next_word_index_verb)
#         if next_word_index_verbs is None:
#             continue

#         next_word_index_noun = row["next_word_index_noun"]
#         next_word_index_nouns = fetch_next_index(next_word_index_noun)
#         if next_word_index_nouns is None:
#             continue

#         next_word_index_adjective = row["next_word_index_adjective"]
#         next_word_index_adjectives = fetch_next_index(next_word_index_adjective)
#         if next_word_index_adjective is None:
#             continue
