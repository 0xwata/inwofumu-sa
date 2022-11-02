# -*- coding: utf-8 -*-

from util.ipa_match_word_searcher import IpaMatchWordSearcher
from util.translate import Translate
from util.tokenizer import Tokenizer, TokenizerSpacy
import csv

BASE_URL = "../data/ipa-dict/data/"
OUTPUT_DIR = "../data/ipa-dict/data/v2"
# LANGS_FOR_SEARCH = ['ja', 'en', 'de', 'id', 'zh-cn', 'ko', 'eo', 'es', 'ro', 'ar', 'is', 'vi', 'sv', 'fr', 'fi']

LANGS_FOR_SEARCH = ['ja']
def add_pos_ipa_dict():
    ipaMatchWordSearcher = IpaMatchWordSearcher()
    translate = Translate()
    tokenizer = TokenizerSpacy()

    for lang in LANGS_FOR_SEARCH:
      output = []
      print(lang)
      ipa_li = ipaMatchWordSearcher.lang_to_ipa_li_for_search[lang]
      print(len(ipa_li))
      count = 0
      for row in ipa_li:
        output_row = []
        word = row[0]
        word_en = translate.translate_to_english_by_language(
          word=word,
          lang=lang
        )
        if word_en == "":
          continue


        request_word_pos = tokenizer.fetch_target_pos(
          word=word,
          word_en=word_en,
          lang=lang
        )
        if request_word_pos == "":
          continue

        output_row.append(request_word_pos)
        output_row.append(row[0])
        output_row.append(row[1])
        output.append(output_row)
        count += 1
        if count % 100 == 0:
          print(f"{count} / {len(ipa_li)}")
      print(f"{count} / {len(ipa_li)}")
      print()
      f = open(f'{OUTPUT_DIR}/{lang}.txt', 'w')
      writer = csv.writer(f, delimiter='\t')
      writer.writerows(output)

if __name__ == "__main__":
  add_pos_ipa_dict()