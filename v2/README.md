## 生成する中間テーブル

### rhyme_pair.csv

create_rhyme_pair.py を実行して生成されるアウトプット
| id | word | word_ipa| word_ipa_rhyme | word_lang| word_en | word_ja | pair_word | pair_word_ipa | pair_word_ipa_rhyme |pair_word_en | pair_word_ja | rhyme_type | match_ipa_rhyme | pos | syllable |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 19 | hoge | oe | oe | ja | ho | hoge | fuga | ua | ua | hoge | fdf | to or kyaku | ou | noun | 3 |

- id: (必要ないかも)
- word: 単語
- word_ipa: 単語 →IPA 変換
- word_ipa_rhyme: 単語 →IPA 変換 → 押韻に必要な IPA 部分だけを抽出
- word_lang: 単語の言語
- word_en: 単語の英訳
- word_ja: 単語の日本語訳
- pair\_\*\* が続く
- rhyme_type: 頭韻 or 脚韻
- match_ipa_rhyme: カスタムルールで抽出した word_ipa_rhyme で韻を踏んでる部分の IPA
- pos: 品詞
- shyllable: 音節

## 最終 output の生成方法

### deliverables/v\*/(押韻)\_(韻のタイプ)\_(音節)\_(品詞).csv

rhyme_pair.csv を入力として create_deliverables.py を実行して生成されるアウトプット

期待値の例

```buildoutcfg
A: uu_kyaku_4_verb : sample, ほじくる, doodle, ひきずる, google
B: oi_to_2_adj : showy, 遠い, sorry, 多い, holy
C: ai_to_2_noun : light, あいつ, dive, type, 細工
D: uo_to_3_adv : slowly, すごく, growly, うとうと, drolly
```

疑似コード（最新は異なる可能性あり）

```python
  unique_pos_group = df["pos"].unique()
  unique_type_group = df["type"].unique()
  unique_rhyme_vowel_list = df_noun_to["rhyme_vowel"].unique()

  for unique_pos in unique_pos_group:
      for unique_type in unique_type_group:
          for unique_rhyme_vowel in unique_rhyme_vowel_list:
              hoge =df[df["pos"] == unique_pos & \
                       df["type"] == unique_type & \
    　　　　　　　       df["rhyme_vowel"] == unique_rhyme_vowel
                      ]
              unique_word_group = hoge["word"].extend(hoge["pair_word"]).unique()
              unique_word_group.to_csv(unique_rhyme_vowel, "_", unique_type, "_", unique_pos, ".csv", )
```
