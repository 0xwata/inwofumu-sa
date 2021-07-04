import pandas as pd
import glob
import re

"""
input:
    request_word,
    request_lang,
    request_pos,
    request_ipa,
    request_ipa_formatted,
    request_word_en,
    response_word,
    response_lang,
    response_pos,
    response_ipa,
    response_ipa_formatted,
    response_word_en

output:
    word（例: 懒散）
    word_language（例: ch)
    word_pos
    word_ipa
    word_ipa_edited_vowel
    word_en(例: Lazy)
    word_translated_by_01(例: 省略)
    word_translated_by_02(例: 省略)
    word_translated_by_03(例: 省略)
    word_translated_by_04(例: 省略)
    next_word_index_verb(例: 145:14:231:31:1）
    next_word_index_noun(例: 145:14:231:31:1）
    next_word_index_adjective(例: 145:14:231:31:1）
"""
request_column = ["request_word","request_lang","request_pos","request_ipa","request_ipa_new_formatted","request_word_en"]
response_column = ["response_word","response_lang","response_pos","response_ipa","response_ipa_new_formatted","response_word_en"]

request_column_rename_dict = {
    "request_word":"word",
    "request_lang":"word_lang",
    "request_pos":"word_pos",
    "request_ipa":"word_ipa",
    "request_ipa_new_formatted":"word_ipa_edited_vowel",
    "request_word_en":"word_en"
}
response_column_rename_dict = {
    "response_word":"word",
    "response_lang":"word_lang",
    "response_pos":"word_pos",
    "response_ipa":"word_ipa",
    "response_ipa_new_formatted":"word_ipa_edited_vowel",
    "response_word_en":"word_en"
}

output_column = ["word", "word_lang", "word_pos", "word_ipa", "word_ipa_edited_vowel", "word_en", "next_word_index_verb", "next_word_index_noun", "next_word_index_adjective"]

N_MATCH = 3

# 識別対象の母音
VOWELS = ["i", "y", "ɨ", "ʉ", "ɯ", "u", "ɪ", "ʏ", "ʊ", "e", "ø", "ɘ", "ɵ", "ɤ", "o", "ə", "ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ", "æ","ɐ", "a", "ɶ", "ɑ", "ɒ", "ɚ", "ɑ˞", "ɔ˞","ɝ", "ʲ"]

VOWELS_STRING = ''.join(VOWELS)

# 似ているアクセントに変換する辞書
SIMILAR_VOWEL_DICT = {
    "i":"y",
    "ʲ":"y",
    "ɨ": "ʉ",
    "ɯ": "u",
    "ɪ": "ʏ",
    "e": "ø",
    "ɤ": "o",
    "ɛ": "œ",
    "ɜ": "ɞ",
    "ʌ": "ɔ",
    "ɔ˞.": "ɔ",
    "a": "ɶ",
    "ɒ": "ɑ",
    "ɑ˞": "ɑ",
    "ɚ": "ə",
    "ɝ": "ə",
}

CONSONANT_PLOSIVE_UNVOICED = ["p", "t", "č", "č", "k", "q"] # -> p
CONSONANT_PLOSIVE_VOICED = ["b", "d", "ǰ", "ɟ", "g", "ɡ", "G", "ʔ"] # -> b
CONSONANT_IMPLOSIVE = ["ɓ", "ɗ", "ɠ"] # -> ɓ
CONSONANT_FRICATIVE_UNVOICED = ["ϕ", "f", "θ", "s", "š", "ɕ", "x", "χ", "ħ"] # -> ϕ
CONSONANT_FRICATIVE_VOICED = ["β", "v", "ð", "z", "ž", "ʑ", "γ", "ʁ", "ʕ"] # -> β
CONSONANT_NASAL = ["m", "ɱ", "n", "ň", "ɲ", "ŋ", "N", "ɴ"] # -> m
CONSONANT_LATERAL_APPPROACH_SOUND = ["l", "Ǐ", "ʎ"] # -> l

CONSONENTS = CONSONANT_PLOSIVE_UNVOICED + CONSONANT_PLOSIVE_VOICED + \
             CONSONANT_IMPLOSIVE + CONSONANT_FRICATIVE_UNVOICED + CONSONANT_FRICATIVE_VOICED + \
             CONSONANT_NASAL + CONSONANT_LATERAL_APPPROACH_SOUND
VOWELS_CONSONENTS = VOWELS + CONSONENTS
VOWELS_CONSONENTS_STRING = ''.join(VOWELS_CONSONENTS)


def create_df(filepath):
    files = glob.glob(filepath)
    print(files)
    for i, file in enumerate(files):
        if i == 0:
            df = pd.read_csv(file, sep=',')
            print(f"count={i}, len(df)={len(df)}")
            continue
        df_tmp = pd.read_csv(file, sep=',')
        print(f"count={i}, len(df)={len(df_tmp)}")
        df = pd.concat([df, df_tmp])
    print(f"len(df)={len(df)}")

    df_d = df[~df.duplicated()]
    df_d_r = df_d.reset_index(drop=True)
    print(len(df))
    print(len(df_d_r))

    return df_d_r


def map_consonents(char):
    result = ""
    if char in CONSONANT_PLOSIVE_UNVOICED \
        or char in CONSONANT_PLOSIVE_VOICED \
        or char in CONSONANT_IMPLOSIVE \
        or char in CONSONANT_FRICATIVE_UNVOICED \
        or char in CONSONANT_FRICATIVE_VOICED \
        or char in CONSONANT_LATERAL_APPPROACH_SOUND:
        result = "b"
    if char in CONSONANT_NASAL:
        result = "m"

    return result

def create_new_format(ipa_word: str) -> str:
    ipa_formatted = ""
    for index, char in enumerate(ipa_word):
        if char in VOWELS:
            if char in SIMILAR_VOWEL_DICT.keys(): #similar_vowel_groupは辞書型
                ipa_formatted  += SIMILAR_VOWEL_DICT[char]
                continue
            ipa_formatted += char
            continue
        ## 以下、子音記号の抽出
        if char in CONSONENTS:
            try:
                next_char = ipa_word[index+1]
                if next_char not in VOWELS:
                    ipa_formatted += map_consonents(char)
            #indexが最後の時も追加する
            except IndexError:
                ipa_formatted += map_consonents(char)
    return ipa_formatted

def fetch_target_vowel(ipa:str) -> str:
    result = ""
    for char in ipa:
        if char in VOWELS_STRING:
            result += char
    return result

def set_word_last_n_char(word: str):
    LAST_N_CHAR = N_MATCH
    word_last_n_char = word[-LAST_N_CHAR:]
    vowel_in_word_last_n_char = fetch_target_vowel(word_last_n_char)
    while len(vowel_in_word_last_n_char) < 3:
        word_last_n_char_previous = word_last_n_char
        LAST_N_CHAR += 1
        word_last_n_char = word[-LAST_N_CHAR:]
        if word_last_n_char == word_last_n_char_previous:
            break
        vowel_in_word_last_n_char = fetch_target_vowel(word_last_n_char)
    return word_last_n_char



def ipa_chain_aggregator():
    df = pd.read_csv("../output/spacy_match-word-augumentation/all_after_screaning.csv", sep=',')
    ## 前のipa_formatのカラムを削除する
    df = df.drop('request_ipa_formatted', axis=1)
    df = df.drop('response_ipa_formatted', axis=1)

    requests = df[request_column]
    requests_renamed = requests.rename(columns=request_column_rename_dict)

    responses = df[response_column]
    responses_renamed =responses.rename(columns=response_column_rename_dict)

    df_concat = pd.concat([requests_renamed, responses_renamed])
    print(df_concat.duplicated().sum())
    print(len(df_concat[~df_concat.duplicated()]))
    df_concat_d = df_concat[~df_concat.duplicated()]
    df_concat_d_r = df_concat_d.reset_index(drop=True)
    print(df_concat_d_r.groupby('word_pos').size())


    output_count = 0
    group_next_word_index_verb = []
    group_next_word_index_noun = []
    group_next_word_index_adjective = []
    match_full_pair_count = 0
    df_concat_d_r_word_lang = df_concat_d_r.word_lang
    df_concat_d_r_word= df_concat_d_r.word
    df_concat_d_r_word_ipa_edited_vowel = df_concat_d_r.word_ipa_edited_vowel
    df_concat_d_r_word_pos = df_concat_d_r.word_pos

    for idx_i in range(df_concat_d_r.shape[0]):
        query_word_ipa_edited_vowel = df_concat_d_r_word_ipa_edited_vowel.iloc[idx_i]
        query_word = df_concat_d_r_word.iloc[idx_i]
        query_lang = df_concat_d_r_word_lang.iloc[idx_i]

        next_word_index_verb = []
        next_word_index_noun = []
        next_word_index_adjective = []
        match_count = 0
        for idx_j in range(df_concat_d_r.shape[0]):
            if df_concat_d_r_word.iloc[idx_j] == query_word or df_concat_d_r_word_lang.iloc[idx_j] == query_lang:
                continue

            if set_word_last_n_char(create_new_format(df_concat_d_r_word_ipa_edited_vowel.iloc[idx_j])) == set_word_last_n_char(query_word_ipa_edited_vowel):
                if df_concat_d_r_word_pos.iloc[idx_j] == "verb":
                    next_word_index_verb.append(str(idx_j))
                elif df_concat_d_r_word_pos.iloc[idx_j] == "adjective":
                    next_word_index_adjective.append(str(idx_j))
                else: # row_j.pos == noun
                    next_word_index_noun.append(str(idx_j))
                match_count += 1

        if len(next_word_index_verb) >= 3 and \
           len(next_word_index_adjective) >= 3 and \
           len(next_word_index_noun) >= 3:
           match_full_pair_count += 1
           print(f"match_full_pair_count:{match_full_pair_count}")
           print(f"match_count:{match_count}")
           print(f"match_count_verb:{len(next_word_index_verb)}")
           print(f"match_count_adjective:{len(next_word_index_adjective)}")
           print(f"match_count_noun:{len(next_word_index_noun)}")
        group_next_word_index_verb.append(":".join(next_word_index_verb))
        group_next_word_index_adjective.append(":".join(next_word_index_adjective))
        group_next_word_index_noun.append(":".join(next_word_index_noun))

        output_count += 1
        print(f"next i->{output_count+1}")

    df_concat_d_r["next_word_index_verb"] = group_next_word_index_verb
    df_concat_d_r["next_word_index_adjective"] = group_next_word_index_adjective
    df_concat_d_r["next_word_index_noun"] = group_next_word_index_noun
    df_concat_d_r[output_column]

    df_concat_d_r.to_csv(f'../output/final/final/output.csv')
    print(f"finish writing output to csv/ {len(df_concat_d_r)}")
    print(f"{match_full_pair_count} / {len(df_concat_d_r)}")

if __name__ == "__main__":
    ipa_chain_aggregator()
