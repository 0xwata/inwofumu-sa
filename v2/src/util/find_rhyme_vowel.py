from model.rhyme_type import RhymeType
from typing import Optional

"""
@param: ipa_str_vowels_1: IPAStringのObjectのプロパティであるvowels
@param; ipa_str_vowels_2: 〃
"""

def find_rhyme_vowel(ipa_str_vowels_1: str, ipa_str_vowels_2: str, rhyme_type: RhymeType) -> Optional[str]:
    rhyme_bowel = ""

    if len(ipa_str_vowels_1) > len(ipa_str_vowels_2):
        a = ipa_str_vowels_1
        b = ipa_str_vowels_2
        max_rhyme_length = len(b)
    else:
        a = ipa_str_vowels_2
        b = ipa_str_vowels_1
        max_rhyme_length = len(b)

    if rhyme_type == RhymeType.TOIN:
        """頭韻判定"""
        for i in range(max_rhyme_length):
            if i == 0:
                continue
            if b.startswith(a[:i + 1]) is True:
                rhyme_bowel += b[i]
            else:
                break
        # 空文字もしくは1文字しか合致しなかった場合は、Noneを返す
        if len(rhyme_bowel) == 0 or len(rhyme_bowel) == 1:
            return None
        else:
            return rhyme_bowel
    else:
        """脚韻判定"""
        for i in range(max_rhyme_length):
            if i == 0:
                continue
            if b.endswith(a[-1 * i:]) is True:  ## 後ろから1文字ずつ追加していって判定していく
                rhyme_bowel += b[-1 * i]
            else:
                break

        # 空文字もしくは1文字しか合致しなかった場合は、Noneを返す
        if len(rhyme_bowel) == 0 or len(rhyme_bowel) == 1:
            return None
        else:
            return rhyme_bowel[::-1]  ## 後ろから1文字ずつ追加しているので最後は反転して渡す
