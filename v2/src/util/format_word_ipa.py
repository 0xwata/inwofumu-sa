
def format_word_ipa(ipa: str) -> str:
    result = ""
    for char in ipa:
        if char == "/" or char == "̠ ":
            continue
        result += char
    return result
