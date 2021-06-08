from selenium import webdriver

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
        'ru': 'russian'
"""


converter_dic = {
    "ja" : "ja",
    "en" : "en",
    "de" : "de",
    "id" : "ma"
    "zh-cn" : "zh"
}

class IpaMatchWordSearcher:
    def __init__(self, ):
        self.converter_dic = converter_dic

    def execute(self, words):
        """[summary]

        Args:
            words ([type]): [description]
        """

        for k, v in words.items():
            # 各翻訳された単語についてIPA変換
            if(k == 'ko'){
                #韓国語のIPA
                #ipa-lookupのページがなかった
                pass
            } else if (k == 'ru') {
                #ロシア語のIPA
                #そもそもhttps://github.com/open-dict-data/ipa-dictにデータがない言語
                pass
            } else {
                ipa = ipa_converter_by_Ipa_lookup(lang = k, word = v)
            }

            # 返還されたIPAをもとに合致する単語を探す





    def ipa_converter_by_Ipa_lookup(self, lang: str, word: str) -> str :
        """[summary]
        入力した単語群をIPAに変換する.
        https://github.com/open-dict-data/ipa-dictを元にしたIPA検索サイトがあったので、
        指定言語のページが存在すれば、そちらで検索をかける。
        Args:
            word (str): [description]

        Returns:
            ipa (str): wordのIPA
        """
        drive_path = 'https://open-dict-data.github.io/ipa-lookup/{lang}/?#'

        print('Chromeを起動中')
        driver = webdriver.Chrome(driver_path)

        #指定したURLに遷移
        driver.get(URL)

        # 画面のロードが完了する前に、処理が走ってしまいエラーになるので数秒待機するように設定する
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Btn')))

        driver.find_element_by_name('From').send_keys(v)
        driver.find_element_by_id('Btn').click()

        element = driver.find_element_by_id('output')
        print(element)

        #終わったら、chromeを終了する
        driver.quit()

        # TODO: <br>~~~<div>で要素抽出→<br>, <div>を削除でipaの要素を抽出する

    def search(self, lang:str, ipa:str) -> dict:
    """[summary]

    Args:
        lang (str): [description]
        ipa (str): [description]

    Returns:
        dict: [description]
    """
