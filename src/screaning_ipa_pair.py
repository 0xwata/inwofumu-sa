from numpy import character
import pandas as pd
import glob

# 識別対象の母音
VOWELS = ["i", "y", "ɨ", "ʉ", "ɯ", "u", "ɪ", "ʏ", "ʊ", "e", "ø", "ɘ", "ɵ", "ɤ", "o", "ə", "ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ", "æ"
                "ɐ", "a", "ɶ", "ɑ", "ɒ", "ɚ", "ɑ˞", "ɔ˞"]

# 似ているアクセントに変換する辞書
SIMILAR_VOWEL_DICT = {
    "i":"y",
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
}

CONSONANT_PLOSIVE_UNVOICED = ["p", "t", "č", "č", "k", "q"] # -> p
CONSONANT_PLOSIVE_VOICED = ["b", "d", "ǰ", "ɟ", "g", "ɡ", "G", "ʔ"] # -> b
CONSONANT_IMPLOSIVE = ["ɓ", "ɗ", "ɠ"] # -> ɓ
CONSONANT_FRICATIVE_UNVOICED = ["ϕ", "f", "θ", "s", "š", "ɕ", "x", "χ", "ħ"] # -> ϕ
CONSONANT_FRICATIVE_VOICED = ["β", "v", "ð", "z", "ž", "ʑ", "γ", "ʁ", "ʕ"] # -> β
CONSONANT_NASAL = ["m", "ɱ", "n", "ň", "ɲ", "ŋ", "N"] # -> m
CONSONANT_LATERAL_APPPROACH_SOUND = ["l", "Ǐ", "ʎ"] # -> l
CONSONANT_CENTER_APPROXIMATION_SOUND =  ["r", "w", "h"] # -> r

CONSONENTS = CONSONANT_PLOSIVE_UNVOICED + CONSONANT_PLOSIVE_VOICED + \
             CONSONANT_IMPLOSIVE + CONSONANT_FRICATIVE_UNVOICED + CONSONANT_FRICATIVE_VOICED + \
             CONSONANT_NASAL + CONSONANT_LATERAL_APPPROACH_SOUND + CONSONANT_CENTER_APPROXIMATION_SOUND

N_MATCH = 3

def create_df():
    files = glob.glob("../output/spacy_match-word-augumentation/*.csv")
    for i, file in enumerate(files):
        if i == 0:
            df = pd.read_csv(file, sep=',')
            print(f"count={i}, len(df)={len(df)}")
            continue
        df_tmp = pd.read_csv(file, sep=',')
        print(f"count={i}, len(df)={len(df_tmp)}")
        df = pd.concat([df, df_tmp])
    print(f"len(df)={len(df)}")

    return df


def map_consonents(char: character) -> character:
    result = ""
    if char in CONSONANT_PLOSIVE_UNVOICED:
        result = "p"
    if char in CONSONANT_PLOSIVE_VOICED:
        result = "b"
    if char in CONSONANT_IMPLOSIVE:
        result = "ɓ"
    if char in CONSONANT_FRICATIVE_UNVOICED:
        result = "ϕ"
    if char in CONSONANT_FRICATIVE_VOICED:
        result = "β"
    if char in CONSONANT_NASAL:
        result = "m"
    if char in CONSONANT_LATERAL_APPPROACH_SOUND:
        result = "l"
    if char in CONSONANT_CENTER_APPROXIMATION_SOUND:
        result = "r"
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

def main():
    df = create_df()
    df.to_csv("../output/spacy_match-word-augumentation/all_before_screaning.csv")


    screaning_flgs = []
    request_ipa_new_formats = []
    response_ipa_new_formats = []
    for index, row in df.iterrows():
        request_ipa = row.request_ipa
        response_ipa = row.response_ipa

        request_ipa_new_format = create_new_format(request_ipa)
        response_ipa_new_format = create_new_format(response_ipa)

        screaning_flg = 0
        if request_ipa_new_format[-N_MATCH:] == response_ipa_new_format[-N_MATCH:]:
            screaning_flg = 1

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

    df_with_flg.to_csv("../output/spacy_match-word-augumentation/all_after_screaning_with_flg.csv")
    df_after_screaning.to_csv("../output/spacy_match-word-augumentation/all_after_screaning.csv")

    print("all_before_screaning.csv:", len(df))
    print("all_after_screaning.csv:", len(df_after_screaning))



if __name__=="__main__":
    main()