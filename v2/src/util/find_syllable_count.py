# -*- coding: utf-8 -*-

from ipapy.ipastring import IPAString


def find_syllable_count(ipa: str) -> int:
    # 3連続の母音の場合は2音でカウントする
    # 例： liar（lάɪɚ）の場合、ラ・ィ・アーになり、音で聴いたときに２音で聴こえる場合が多いため。
    syllable_count = 0
    sequence_vowel_count = 0
    try:
        s_ipa = IPAString(unicode_string=ipa)
        letters = s_ipa.letters
        vowels = s_ipa.vowels
        print(vowels)
        print(letters)
        for char in s_ipa.letters:
            if sequence_vowel_count == 2:
                syllable_count -= 1
                # TODO: 4連続以上は考える必要あるか？
                sequence_vowel_count = 0 
            if char in vowels:
                syllable_count += 1
                sequence_vowel_count += 1
            else:
                sequence_vowel_count = 0

    except ValueError as e:
        syllable_count = -1
    print(syllable_count)
    return syllable_count


if __name__ == "__main__":
    find_syllable_count(u"laɪər")