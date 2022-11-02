from model.rhyme_type import RhymeType
from typing import Optional
import random
"""
TODO: 正確にはVowel（母音）だけじゃないからメソッド名変えた方が良さそう
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
            if b.endswith(a[-1 * i:]) is True:  # 後ろから1文字ずつ追加していって判定していく
                rhyme_bowel += b[-1 * i]
            else:
                break

        # 空文字もしくは1文字しか合致しなかった場合は、Noneを返す
        if len(rhyme_bowel) == 0 or len(rhyme_bowel) == 1:
            return None
        else:
            # 後ろから1文字ずつ追加しているので最後は反転して渡す
            return rhyme_bowel[::-1]


def check_ipa_rhyme_match(ipa_rhyme_1: str, ipa_rhyme_2: str, rhyme_type: RhymeType) -> Optional[str]:
    match_ipa_rhyme = ""

    if len(ipa_rhyme_1) > len(ipa_rhyme_2):
        a = ipa_rhyme_1
        b = ipa_rhyme_2
        max_rhyme_length = len(b)
    else:
        a = ipa_rhyme_2
        b = ipa_rhyme_1
        max_rhyme_length = len(b)

    if rhyme_type == RhymeType.TOIN:
        """頭韻判定"""
        for i in range(max_rhyme_length):
            if i == 0:
                continue
            elif b.startswith(a[:i + 1]) is True:
                match_ipa_rhyme += b[i]
            else:
                break
        # 空文字もしくは1文字しか合致しなかった場合は、Noneを返す
        if len(match_ipa_rhyme) == 0 or len(match_ipa_rhyme) == 1:
            return None
        else:
            if len(match_ipa_rhyme) > 2:
                return match_ipa_rhyme
            else: # 2文字で韻を踏んでる場合は3割採用
                isAccept = random.choices([True, False], weights=[0.3, 0.7], k=1)
                if isAccept:
                    return match_ipa_rhyme
                else:
                    return None
    else:
        """脚韻判定"""
        for i in range(max_rhyme_length):
            if i == 0:
                continue
            # 後ろから1文字ずつ追加していって判定していく
            elif b.endswith(a[-1 * i:]) is True:
                match_ipa_rhyme += b[-1 * i]
            else:
                break

        # 空文字もしくは1文字しか合致しなかった場合は、Noneを返す
        if len(match_ipa_rhyme) == 0 or len(match_ipa_rhyme) == 1:
            return None
        else:
            if len(match_ipa_rhyme) == 2:
                isAccept = random.choices([True, False], weights=[0.3, 0.7], k=1)
                if isAccept:
                    # 後ろから1文字ずつ追加しているので最後は反転して渡す
                    return match_ipa_rhyme[::-1]
                else:
                    return None
