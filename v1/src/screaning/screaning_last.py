# -*- coding: utf-8 -*-
import pandas as pd

black_list = ["Fugó.", "Abréviasi。", "○", "Amhar。", "Chicharranda。", ]
def isEnglish(s):
    print(s)
    if type(s) == float:
        return True
    if s in black_list:
        return True
    if "。" in s or "." in s:
        return True
    try:
        for char in s:
            char.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def isenglish(s):
    print("en+"+str(s))
    if type(s) == float:
        return False
    is_capital = False
    for char in s:
        if char.isupper():
            is_capital = True
    if is_capital == True:
        return False

    if s.isupper() == True:
        return False
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


output_column = ["word", "word_lang", "word_pos", "word_ipa", "word_ipa_edited_vowel", "word_en", "next_word_index_verb", "next_word_index_noun", "next_word_index_adjective", "word_ch", "word_id", "word_ja"]

df = pd.read_csv("../../output/final/final/output_after_screaning_v4.csv", sep=',', index_col=0)
print(df.columns)
df_ja_screaning = df[df["word_ja"] != ""]
df_ja_screaning["word_ja_bool"] = df_ja_screaning["word_ja"].apply(isEnglish)

df_ja_screaning["word_en_bool"] = df_ja_screaning["word_en"].apply(isenglish)

df_ja_screaning_screaning = df_ja_screaning[(df_ja_screaning["word_ja_bool"] == False) & (df_ja_screaning["word_en_bool"] == True)]
print(len(df_ja_screaning_screaning))


df_ja_screaning_screaning[output_column]

print(len(df_ja_screaning_screaning))
df_ja_screaning_screaning.to_csv(f'../output/final/final/output_after_screaning_v4_ja_screaning.csv')
