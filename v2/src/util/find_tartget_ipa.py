# 識別対象の母音
VOWELS = ["i", "y", "ɨ", "ʉ", "ɯ", "u", "ɪ", "ʏ", "ʊ", "e", "ø", "ɘ", "ɵ", "ɤ", "o", "ə", "ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ",
          "æ", "ɐ", "a", "ɶ", "ɑ", "ɒ", "ɚ", "ɑ˞", "ɔ˞", "ɝ", "ʲ"]

VOWELS_STRING = ''.join(VOWELS)

# 似ているアクセントに変換するマッピング
SIMILAR_VOWEL_DICT = {
    "i": "y",
    "ʲ": "y",
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

# 識別対象とする子音
CONSONANT_PLOSIVE_UNVOICED = ["p", "t", "č", "č", "k", "q"]  # -> p
CONSONANT_PLOSIVE_VOICED = ["b", "d", "ǰ", "ɟ", "g", "ɡ", "G", "ʔ"]  # -> b
CONSONANT_IMPLOSIVE = ["ɓ", "ɗ", "ɠ"]  # -> ɓ
CONSONANT_FRICATIVE_UNVOICED = ["ϕ", "f", "θ", "s", "š", "ɕ", "x", "χ", "ħ"]  # -> ϕ
CONSONANT_FRICATIVE_VOICED = ["β", "v", "ð", "z", "ž", "ʑ", "γ", "ʁ", "ʕ"]  # -> β
CONSONANT_NASAL = ["m", "ɱ", "n", "ň", "ɲ", "ŋ", "N", "ɴ"]  # -> m
CONSONANT_LATERAL_APPROACH_SOUND = ["l", "Ǐ", "ʎ"]  # -> l

CONSONANTS = CONSONANT_PLOSIVE_UNVOICED + CONSONANT_PLOSIVE_VOICED + \
             CONSONANT_IMPLOSIVE + CONSONANT_FRICATIVE_UNVOICED + CONSONANT_FRICATIVE_VOICED + \
             CONSONANT_NASAL + CONSONANT_LATERAL_APPROACH_SOUND
VOWELS_CONSONANTS = VOWELS + CONSONANTS
VOWELS_CONSONANTS_STRING = ''.join(VOWELS_CONSONANTS)


def find_target_ipa(ipa: str) -> str:
    """[summary]
    対象のIPAに変換するメソッド
    Args:
        ipa (str): 例：/ˌkɔɹəˈspɑndənt/（corespondentのIPA)。複数のIPAは返って来ない仕様（今のところ）

    Returns:
        str: 入力したipaの母音を抽出し、連結し、文字列で返却 例：'ɔəɑə'
    """
    result = ""
    for char in ipa:
        if char in VOWELS_CONSONANTS_STRING:
            result += char
    return result


def find_target_ipa_rhyme(word: str) -> str:
    """[summary
    対象のIPAに変換し、更に似ているアクセントにマッピングして文字列を返すメソッド
    """
    ipa_rhyme = ""
    for index, char in enumerate(word):
        if char in VOWELS:
            if char in SIMILAR_VOWEL_DICT.keys():  # similar_vowel_groupは辞書型
                ipa_rhyme += SIMILAR_VOWEL_DICT[char]
            else:
                ipa_rhyme += char
        elif char in CONSONANTS:
            try:
                next_char = word[index + 1]
                if next_char not in VOWELS:
                    ipa_rhyme += map_consonants(char)
            # indexが最後の時も追加する
            except IndexError:
                ipa_rhyme += map_consonants(char)
    return ipa_rhyme


def map_consonants(char):
    result = ""
    if char in CONSONANT_PLOSIVE_UNVOICED \
            or char in CONSONANT_PLOSIVE_VOICED \
            or char in CONSONANT_IMPLOSIVE \
            or char in CONSONANT_FRICATIVE_UNVOICED \
            or char in CONSONANT_FRICATIVE_VOICED \
            or char in CONSONANT_LATERAL_APPROACH_SOUND:
        result = "b"
    if char in CONSONANT_NASAL:
        result = "m"

    return result
