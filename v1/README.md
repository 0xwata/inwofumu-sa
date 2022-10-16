# inwofumu-sa
SIGGRAPH ASIA 2021に応募する作品のマルチリンガルな韻ペアを収集するスクリプトのリポジトリです。

## 導入

セットアップ

1. /dataで、ipa_dict(https://github.com/open-dict-data/ipa-dict)をclone
2. pip install -r requirements.txt
3. python nltk_download.py
4. python -m spacy download zh_core_web_sm(main.pyを実行して怒られる物をインストールしていく)

## ファイル説明（雑)

* main.py(ipaで一致する単語を収集するスクリプト)
    * ipa_match_word_searcher.py
* screaning_ipa_pair.py(収集したペアのスクリーニングを行うスクリプト)
* ipa_chain_aggregator.py(最終アウトプットの雛形作成 && next_indexを貼る作業を行うスクリプト)
* screaning_next_search_index.py(next_indexが3つ以上ない行は削除するスクリプト)
* ipa_chain_aggregator_after_screaning_next_search_index.py(screaning_next_search_indexを実行した後に、next_indexを再度貼るスクリプト)
* tralslate_mother_tongue.py()

* create_collocations_data.py(コロケーションを収集するスクリプト)
* create_collocations_column.py(コロケーションを検索して、最終アウトプットにcollocationのカラムを作成するスクリプト)

## 大枠の流れ

1. main.py
2. screaning_ipa_pair.py
3. ipa_chain_aggregator.py
4. screaning_next_search_index
5. ipa_chain_aggregator_after_screaning_next_search_index
6. アウトプットの行数が変わらなくなるまで、4~5を繰り返す
7. tralslate_mother_tongue,py

※末尾にラストと書いてあるファイルは、当日に突貫で作成したファイル。

## 最終output
カラム
```.csv
・word ##対象単語
・word_lang ##対象単語の言語
・word_pos ##対象単語の品詞
・word_ipa ##対象単語のIPA
・word_ipa_edited_vowel ##IPA検索でマッチした整形済みIPA
・word_en ##デバッグ用に対象単語の英語翻訳
・next_word_index_verb ## 対象単語とIPAマッチした動詞のリスト（カンマ区切りの文字列）
・next_word_index_noun ## 対象単語とIPAマッチした名詞のリスト（カンマ区切りの文字列）
・next_word_index_adjective ## ## 対象単語とIPAマッチした形容詞のリスト（カンマ区切りの文字列）
・word_ch ## 下に表示する言語（中国語)
・word_id ## 下に表示する言語(インドネシア語)
・word_ja ## 下に表示する言語(日本語)
```

## LICENSE
### Random Words
* wonderwords

### IPA
* ipa-dict(https://github.com/open-dict-data/ipa-dict)

### translation(補足：https://qiita.com/_yushuu/items/83c51e29771530646659)
* googletrans==4.0.0-rc1

### POS(Part-of-speech)
* nltk
* spacy

