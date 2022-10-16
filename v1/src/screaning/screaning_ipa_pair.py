from numpy import character
import pandas as pd
import glob
import re

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

N_MATCH = 3

def create_df(filepath):
    files = glob.glob(filepath)
    print(files)
    for i, file in enumerate(files):
        if i == 0:
            df = pd.read_csv(file, sep=',')
            print(f"count={i}, len(df)={len(df)}")
            continue
        df_tmp = pd.read_csv(file, sep=',')
        df = pd.concat([df, df_tmp])

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

def is_first_letter_upper_char(word: str) -> bool:
    return word[0].isupper()

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

def fetch_target_vowel_and_consonents(ipa:str) -> str:
    result = ""
    for char in ipa:
        if char in VOWELS_CONSONENTS_STRING:
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


def main():
    df = create_df("../output/spacy_match-word-augumentation/*.csv")
    df_1 = create_df("../output/*.csv")
    print(len(df),len(df_1))
    df = pd.concat([df, df_1])
    print(len(df))
    df = df[~df.duplicated()]
    df = df.reset_index(drop=True)
    print(len(df))

    df.to_csv("../output/spacy_match-word-augumentation/all_before_screaning.csv")


    screaning_flgs = []
    request_ipa_new_formats = []
    response_ipa_new_formats = []
    for _, row in df.iterrows():
        request_word = row.request_word
        response_word = row.response_word

        request_ipa = row.request_ipa
        response_ipa = row.response_ipa

        request_lang = row.request_lang
        response_lang = row.response_lang

        request_ipa_formatted = row.request_ipa_formatted
        response_ipa_formatted = row.response_ipa_formatted


        request_ipa_new_format = create_new_format(fetch_target_vowel_and_consonents(request_ipa))
        response_ipa_new_format = create_new_format(fetch_target_vowel_and_consonents(response_ipa))

        screaning_flg = 0
        request_ipa_new_format_last_n_char = set_word_last_n_char(request_ipa_new_format)
        response_ipa_new_format_last_n_char = set_word_last_n_char(response_ipa_new_format)


        ## TODO: シラブルの数を制限
        request_flag = 0
        if request_ipa_new_format_last_n_char == response_ipa_new_format_last_n_char:
            request_flag = 1
            if request_lang == "en":
                if is_first_letter_upper_char(request_word):
                    request_flag = 0

            response_flag = 1
            if response_lang == "en":
                if is_first_letter_upper_char(response_word):
                    response_flag = 0

            if len(request_ipa_new_format) > 5 or len(request_ipa_new_format) > 5:
                response_flag = 0

            if request_flag == 1 and response_flag == 1:
                screaning_flg = 1

        # if screaning_flg == 0:
        #     print(0)
        #     print(request_word, request_ipa, request_ipa_formatted, request_ipa_new_format, request_ipa_new_format_last_n_char)
        #     print(response_word, response_ipa, response_ipa_formatted, response_ipa_new_format, request_ipa_new_format_last_n_char)
        #     print()
        # else:
        #     print(1)
        #     print(request_word, request_ipa, request_ipa_formatted, request_ipa_new_format, request_ipa_new_format_last_n_char)
        #     print(response_word, response_ipa, response_ipa_formatted, response_ipa_new_format, request_ipa_new_format_last_n_char)
        #     print()


        screaning_flgs.append(screaning_flg)
        request_ipa_new_formats.append(request_ipa_new_format)
        response_ipa_new_formats.append(response_ipa_new_format)
    print("new formatting 完了")

    df["request_ipa_new_formatted"] = request_ipa_new_formats
    df["response_ipa_new_formatted"] = response_ipa_new_formats
    df["screaning_flg"] = screaning_flgs

    output = ["request_word", "request_lang", "request_pos", "request_ipa", "request_ipa_new_formatted", "request_ipa_formatted", "request_word_en",
               "response_word", "response_lang", "response_pos", "response_ipa", "response_ipa_new_formatted", "response_ipa_formatted", "response_word_en","screaning_flg"]
    df_with_flg = df[output]
    df_after_screaning = df_with_flg[df_with_flg.screaning_flg == 1].drop('screaning_flg', axis=1)
    
    df_after_screaning = df_after_screaning[~df_after_screaning.duplicated()]
    df_after_screaning = df_after_screaning.reset_index(drop=True)

    df_with_flg.to_csv("../output/spacy_match-word-augumentation/all_after_screaning_with_flg.csv")
    df_after_screaning.to_csv("../output/spacy_match-word-augumentation/all_after_screaning.csv")

    print("all_before_screaning.csv:", len(df))
    print("all_after_screaning.csv:", len(df_after_screaning))



if __name__=="__main__":
    main()