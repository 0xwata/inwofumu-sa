from ipapy.ipastring import IPAString


def find_syllable_count(ipa: str) -> int:
    syllable_count = 0
    try:
        s_ipa = IPAString(unicode_string=ipa)
        vowels = s_ipa.vowels
        syllable_count = len(vowels)
    except ValueError as e:
        print(e)
        syllable_count = -1
    return syllable_count
