from numpy import NaN, nan
import pandas as pd
import glob
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import time
import numpy as np

df = pd.read_csv("../output/final/final/output_after_screaning.csv", sep=',', index_col=0)
df_collocations = pd.read_csv('../output/collocations/collocations_with_screaning.csv', index_col=0)
df_collocations['word'] = df_collocations['word'].str.lower() # OK

output_column = ["word", "word_lang", "word_pos", "word_ipa", "word_ipa_edited_vowel", "word_en", "next_word_index_verb", "next_word_index_noun", "next_word_index_adjective", "collocation_word_index_verb", "collocation_word_index_noun", "collocation_word_index_adjective"]

print(df.columns)
print(len(df))
df_word_en = df[["word_en"]]
df_word_pos = df[["word_pos"]]

group_collocation_word_index_verb = []
group_collocation_word_index_noun = []
group_collocation_word_index_adjective = []
output_count = 0
match_collocation_count = 0
for idx in range(df.shape[0]):
    print(idx)
    word = df_word_en.iloc[idx]
    pos = df_word_pos.iloc[idx]
    collocation_word_index_verb = []
    collocation_word_index_noun = []
    collocation_word_index_adjective = []

    # word = NaNの時のため
    if type(word.values[0]) == float:
        group_collocation_word_index_verb.append(":".join(collocation_word_index_verb))
        group_collocation_word_index_noun.append(":".join(collocation_word_index_noun))
        group_collocation_word_index_adjective.append(":".join(collocation_word_index_adjective))
        continue
    df_collocations_hit = df_collocations[df_collocations["word"] == word.values[0].lower()]
    if len(df_collocations_hit) == 0:
        group_collocation_word_index_verb.append(":".join(collocation_word_index_verb))
        group_collocation_word_index_noun.append(":".join(collocation_word_index_noun))
        group_collocation_word_index_adjective.append(":".join(collocation_word_index_adjective))
        continue

    if pos.values[0] == "verb":
        print("hit verb")
        df_collocations_hit_verb = df_collocations_hit[df_collocations_hit.collocation_relation == "V:obj:N"]
        for idx_verb in range(df_collocations_hit_verb.shape[0]):
            collocation_word_verb_raw = df_collocations_hit_verb.collocation_word.iloc[idx_verb]
            print(collocation_word_verb_raw)
            # example: to become blue
            collocation_word_verb_raw_li = collocation_word_verb_raw.split(" ")
            if len(collocation_word_verb_raw_li) != 3:
                continue
            # collocation_word_raw_li[0] = to
            # collocation_word_raw_li[1] = verb
            # collocation_word_raw_li[2] = noun
            if collocation_word_verb_raw_li[1].lower() != word.values[0].lower():
                continue
            query_word_noun = collocation_word_verb_raw_li[2]
            try:
                collocation_word_noun_index = df_word_en.index.get_loc(query_word_noun)
                collocation_word_index_noun.append(str(collocation_word_noun_index))
            except KeyError:
                continue

    if pos.values[0] == "adjective":
        print("hit adjective")
        df_collocations_hit_adjective = df_collocations_hit[df_collocations_hit.collocation_relation == "N:mod:A"]
        for idx_adjective in range(df_collocations_hit_adjective.shape[0]):
            collocation_word_adjective_raw = df_collocations_hit_adjective.collocation_word.iloc[idx_adjective]
            # example: blue necktie
            collocation_word_adjective_raw_li = collocation_word_adjective_raw.split(" ")
            if len(collocation_word_adjective_raw_li) != 2:
                continue
            # collocation_word_raw_li[0] = blue
            # collocation_word_raw_li[1] = necktie
            if collocation_word_adjective_raw_li[0].lower() != word.values[0].lower():
                continue
            query_word_noun = collocation_word_adjective_raw_li[1]
            try:
                collocation_word_noun_index = df_word_en.index.get_loc(query_word_noun)
                collocation_word_index_noun.append(str(collocation_word_noun_index))
            except KeyError:
                continue

    if pos.values[0] == "noun":
        print("hit noun")
        df_collocations_hit_verb = df_collocations_hit[df_collocations_hit.collocation_relation == "V:obj:N"]
        df_collocations_hit_adjective = df_collocations_hit[df_collocations_hit.collocation_relation == "N:mod:A"]
        df_collocations_hit_noun = df_collocations_hit[df_collocations_hit.collocation_relation == "N:nn:N"]

        # verb
        for idx_verb in range(df_collocations_hit_verb.shape[0]):
            collocation_word_verb_raw = df_collocations_hit_verb.collocation_word.iloc[idx_verb]
            # example: to become blue
            collocation_word_verb_raw_li = collocation_word_verb_raw.split(" ")
            if len(collocation_word_verb_raw_li) != 3:
                continue
            # collocation_word_raw_li[0] = to
            # collocation_word_raw_li[1] = verb
            # collocation_word_raw_li[2] = noun
            if collocation_word_verb_raw_li[1].lower() != word.values[0].lower():
                continue
            query_word_noun = collocation_word_verb_raw_li[2]
            try:
                collocation_word_noun_index = df_word_en.index.get_loc(query_word_noun)
                collocation_word_index_noun.append(str(collocation_word_noun_index))
            except KeyError:
                continue

        # adjective
        for idx_adjective in range(df_collocations_hit_adjective.shape[0]):
            collocation_word_adjective_raw = df_collocations_hit_adjective.collocation_word.iloc[idx_adjective]
            # example: blue necktie
            collocation_word_adjective_raw_li = collocation_word_adjective_raw.split(" ")
            if len(collocation_word_adjective_raw_li) != 2:
                continue
            # collocation_word_raw_li[0] = blue
            # collocation_word_raw_li[1] = necktie
            # 一応、小文字に変換して比較する。
            if collocation_word_adjective_raw_li[0].lower() != word.values[0].lower():
                continue
            query_word_noun = collocation_word_adjective_raw_li[1]
            try:
                collocation_word_noun_index = df_word_en.index.get_loc(query_word_noun)
                collocation_word_index_noun.append(str(collocation_word_noun_index))
            except KeyError:
                continue

        # noun
        for idx_noun in range(df_collocations_hit_noun.shape[0]):
            collocation_word_noun_raw = df_collocations_hit_noun.collocation_word.iloc[idx_noun]
            # example: trap door
            collocation_word_noun_raw_li = collocation_word_noun_raw.split(" ")
            if len(collocation_word_noun_raw_li) != 2:
                continue
            # collocation_word_raw_li[0] = blue
            # collocation_word_raw_li[1] = necktie
            if collocation_word_noun_raw_li[0].lower() == word.values[0].lower():
                query_word_noun = collocation_word_adjective_raw_li[1]
            elif collocation_word_noun_raw_li[1].lower() == word.values[0].lower():
                query_word_noun = collocation_word_adjective_raw_li[0]
            else:
                continue

            try:
                collocation_word_noun_index = df_word_en.index.get_loc(query_word_noun)
                collocation_word_index_noun.append(str(collocation_word_noun_index))
            except KeyError:
                continue

    if len(collocation_word_index_verb) > 0 or \
        len(collocation_word_index_adjective) > 0 or \
        len(collocation_word_index_noun) > 0:
           match_collocation_count += 1
           print(f"match_full_pair_count:{match_collocation_count}")
           print(f"match_count_verb:{len(collocation_word_index_verb)}")
           print(f"match_count_adjective:{len(collocation_word_index_adjective)}")
           print(f"match_count_noun:{len(collocation_word_index_verb)}")

    group_collocation_word_index_verb.append(":".join(collocation_word_index_verb))
    group_collocation_word_index_noun.append(":".join(collocation_word_index_noun))
    group_collocation_word_index_adjective.append(":".join(collocation_word_index_adjective))

    output_count += 1
    print(f"next i->{output_count+1}")

df["collocation_word_index_verb"] = group_collocation_word_index_verb
df["collocation_word_index_adjective"] = group_collocation_word_index_adjective
df["collocation_word_index_noun"] = group_collocation_word_index_noun
df[output_column]

df.to_csv(f'../output/final/final/output_after_screaning_with_collocations.csv')
print(f"finish writing output to csv/ {len(df)}")
