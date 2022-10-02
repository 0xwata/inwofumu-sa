

## 生成する中間テーブル
### rhyme_table

|id|word|pair_id|pair_word|type|rhyme_vowel|pos|
|----|----|----|----|----|----|----|
|19|hoge|40||fuga|to or kyaku|ou|noun|

* id:
* pair_id:
* type: 頭韻 or 脚韻
* rhyme_vowel: 韻を踏んでる母音
* pos: 品詞

## 最終outputの生成方法

期待値
```buildoutcfg
A: uu_kyaku_4_verb : sample, ほじくる, doodle, ひきずる, google
B: oi_to_2_adj : showy, 遠い, sorry, 多い, holy
C: ai_to_2_noun : light, あいつ, dive, type, 細工
D: uo_to_3_adv : slowly, すごく, growly, うとうと, drolly
```

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
