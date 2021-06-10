from translate import Translate
from tokenizer import Tokenizer
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_binary
import re
import time

"""
対象言語：
    ・日本語:
        ja.txt
    ・英語:
        en_US.txt
    ・ドイツ語:
        de.txt
    ・インドネシア語:
        ma.txt Malay (Malaysian and Indonesian)
    ・中国語:
        yue.txt Cantonese
        zh_hans.txt(simplified), zh_hant.txt(traditional) Mandarin
    ・韓国語:
        ko.txt Korean
    ・ロシア語
        https://github.com/open-dict-data/ipa-dict/tree/master/data
        ここにデータがない
"""

CONVERTER_DIC_FOR_URL = {
    "ja" : "ja",
    "en" : "en",
    "de" : "de",
    "id" : "ma",
    "zh-cn" : "zh"
}

BASE_URL = "../data/ipa-dict/data/"

# https://www.ipachart.com/
# 上記のvowelを採用する
VOWELS = ["i", "y", "ɨ", "ʉ", "ɯ", "u", "ɪ", "ʏ", "ʊ", "e", "ø", "ɘ", "ɵ", "ɤ", "o", "ə", "ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ", "æ", "ɐ", "a", "ɶ", "ɑ", "ɒ"]

LANGS_FOR_SEARCH = ["ja", "en", "de", "id", "'zh-cn", "ko"]

class IpaMatchWordSearcher:
    def __init__(self):
        self.converter_dic_for_url = CONVERTER_DIC_FOR_URL
        self.ipa_ja_li = self.read_ipa_data(lang = "ja")
        self.ipa_en_li = self.read_ipa_data(lang = "en_US")
        self.ipa_de_li = self.read_ipa_data(lang = "de")
        self.ipa_id_li = self.read_ipa_data(lang = "ma")
        self.ipa_cn_li = self.read_ipa_data(lang = "zh_hans")
        self.ipa_ko_li = self.read_ipa_data(lang = "ko")
        self.lang_to_ipa_li_for_search = {
            "ja": self.ipa_ja_li,
            "en": self.ipa_en_li,
            "de": self.ipa_de_li,
            "id": self.ipa_id_li,
            "zh-cn": self.ipa_cn_li,
            "ko": self.ipa_ko_li
        }

    def read_ipa_data(self, lang:str) -> list:
        """[summary]

        Args:
            lang (str): [description]

        Returns:
            list:
                中身：単語 \t IPA
        """
        ipa_list = []
        with open(BASE_URL + lang + ".txt") as file:
            for s_line in file:
                ipa_list.append(s_line.split('\t'))
        print(lang+".textの読み込みを完了")
        return ipa_list

    def execute(self, words: dict, pos: str):
        """[summary]

        Args:
            words ([dict]): [description]
            pos ([str]): part of speech
        """

        for k, v in words.items():
            # 各翻訳された単語についてIPA変換
            if k == 'ko':
                #韓国語のIPA
                #ipa-lookupのページがなかった
                # TODO: 処理記載する
                continue
            elif k == 'ru':
                #ロシア語のIPA
                #そもそもhttps://github.com/open-dict-data/ipa-dictにデータがない言語
                continue
            else:
                ipa = self.convert_by_ipa_lookup(lang = k, word = v)
                time.sleep(5)

            # IPAの中から、母音の部分を抜き出す
            ipa_vowel = self.detect_vowel(ipa = ipa)

            # 母音で合致する単語を探す
            response_lang, response_word = self.search(lang = k, ipa_vowel = ipa_vowel, pos = pos)

            if(lang != "" & word != ""):
                request_lang = k
                request_word = v
                break

        return {"word": request_word,"lang": request_lang}, {"word": response_word,"lang": response_lang}

    def search(self, lang:str, ipa_vowel:str, pos:str) -> list:
        """[summary]

        Args:
            lang (str): [description]
            vowel (str): [description]

        Returns:
            list: list[0]= lang, list[1]=word
        """
        # 指定した言語以外を探索するように。
        search_lang_li = list(filter(lambda x: x != lang_remove, LANGS_FOR_SEARCH))
        # ランダムに並び替える
        random_index = random.randrange(len(self.nouns))
        search_lang_random_li = search_lang_li[random_index]

        joined_vowels = ''.join(VOWELS)
        flg = False
        lang = ""
        word = ""
        for i in search_lang_random_li:
            ipa_li = self.lang_to_ipa_li_for_search[i]
            for line in ipa_li:
                #line[0]:単語 line[1]:IPA

                # カンマ区切りで複数のIPAが記載されている場合があるので、簡便のため、最初の要素だけ抽出
                ipa_in_line = line[1].split(",")[0] if ("," in line[1]) else line[1]

                ipa_vowel_in_line = ''.join(re.findall('['+joined_vowels+']+', ipa_in_line))

                if(ipa_vowel == ipa_vowel_in_line):
                    word = line[0]
                    lang = i
                    """
                    マッチング済み単語の翻訳処理
                    """
                    word_en = Translate().translate_to_english_by_language(word)

                    """
                    マッチング済み単語の品詞推定処理
                    """
                    pos_flg = Tokenizer().is_target_pos(word = word_en, target_pos = pos)

                    if pos_flg:
                        print("Found the word matched IPA vowel")
                        flg = True
                        break
            if flg:
                print("Loop stop")
                break
        print("Loop finish")
        return [lang, word]



    def detect_vowel(self, ipa:str) -> str:
        """[summary]
        https://www.ipachart.com/
        ここのvowelを採用する

        Args:
            ipa (str): 例：/ˌkɔɹəˈspɑndənt/（corespondentのIPA)。複数のIPAは返って来ない仕様（今のところ）

        Returns:
            str: 入力したipaの母音を抽出し、連結し、文字列で返却 例：'ɔəɑə'
        """
        joined_vowels = ''.join(VOWELS)
        return ''.join(re.findall('['+joined_vowels+']+', ipa))

    def convert_by_ipa_lookup(self, lang: str, word: str) -> str :
        """[summary]
        入力した単語群をIPAに変換する.
        https://github.com/open-dict-data/ipa-dictを元にしたIPA検索サイトがあったので、
        指定言語のページが存在すれば、そちらで検索をかける。
        Args:
            word (str): [description]

        Returns:
            ipa (str): wordのIPA
        """
        lang_path = self.converter_dic_for_url[lang]
        driver_path = 'https://open-dict-data.github.io/ipa-lookup/{lang_path}'.format(lang_path = lang_path)

        print("path:", driver_path)

        print('Chromeを起動中')
        # webdriverのダウンロードが必要
        driver = webdriver.Chrome()

        #指定したURLに遷移
        driver.get(driver_path)

        # 画面のロードが完了する前に、処理が走ってしまいエラーになるので数秒待機するように設定する
        wait = WebDriverWait(driver, 20)

        driver.find_element_by_id('input').send_keys(word)
        # driver.find_element_by_name('FORM').send_keys(word)
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn')))

        driver.find_element_by_class_name('btn').click()


        time.sleep(5)

        # driver.find_element_by_id('Btn').click()

        # element = driver.find_element_by_xpath("//div[@id='output']").text

        element = driver.find_element_by_id('output')
        print(element.text)


        # TODO: <br>~~~<div>で要素抽出→<br>, <div>を削除でipaの要素を抽出する
        ipa = re.findall('<br>(.*)', element)
        print(ipa)

        #終わったら、chromeを終了する
        driver.quit()
        # TODO: 複数のIPAが出力されることがある（レアケース）のでリストで返す？
        # 一旦、複数のresponseの場合は、先頭のIPAを採用する
        return ipa.split(",")[0] if (","  in ipa) else ipa
