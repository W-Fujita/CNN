import requests
from urllib import parse
from bs4 import BeautifulSoup
import json

search_word = ["dog", "cat"] #検索ワード
limit = 1000 #画像の取得枚数の上限

class Google:
    def __init__(self):
        self.SEARCH_URL = "https://www.google.co.jp/search"
        self.session = requests.session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"})

    def search(self, keyword, type, maximum):
        """Google検索"""
        print("Google {} Search: {}".format(type.capitalize(), keyword))
        result = []
        total = 0
        query = self.query_gen(keyword, type)
        while True:
            #検索
            html = self.session.get(next(query)).text
            links = self.get_links(html, type)
            #検索結果の追加
            if not len(links):
                print("-> No more links")
                break
            elif len(links) > maximum - total:
                result += links[:maximum - total]
                break
            else:
                result += links
                total += len(links)
        print("-> 結果{}のlinksを取得しました".format(str(len(result))))
        return result

    def query_gen(self, keyword, type):
        """検索クエリジェネレータ"""
        page = 0
        while True:
            if type == "text":
                params = parse.urlencode({
                    "q": keyword,
                    "num": "100",
                    "filter": "0",
                    "start": str(page * 100)})
            elif type == "image":
                params = parse.urlencode({
                    "q": keyword,
                    "tbm": "isch",
                    "filter": "0",
                    "ijn": str(page)})
            yield self.SEARCH_URL + "?" + params
            page += 1

    def get_links(self, html, type):
        """リンク取得"""
        soup = BeautifulSoup(html, "lxml")
        if type == "text":
            elements = soup.select(".rc > .r > a")
            links = [e["href"] for e in elements]
        elif type == "image":
            elements = soup.select(".rg_meta.notranslate")
            jsons = [json.loads(e.get_text()) for e in elements]
            links = [js["ou"] for js in jsons]
        return links


def main():
    import os
    os.makedirs("./Original", exist_ok=True) #スクレイピングで取得した画像用フォルダ
    bar_template = "\r{0}% [{1}]"

    #画像のURLをgoogle検索から取得する
    google = Google()
    for word in search_word:
        img_URLs = google.search(word, "image", limit) #画像検索
        os.makedirs("./Original/"+str(word), exist_ok=True) #保存先のフォルダの作成
        #Originalファイルに画像を保存する
        for i,target in enumerate(img_URLs): #img_URLsからtargetに入れる
            try:
                re = requests.get(target, allow_redirects=False)
                with open("./Original/"+str(word)+"/"+str(i)+".jpg", "wb") as f: #Originalフォルダに格納
                    f.write(re.content) #.contentで画像データとして書き込む
            except requests.exceptions.ConnectionError:
                continue
            except UnicodeEncodeError:
                continue
            except UnicodeError:
                continue
            except IsADirectoryError:
                continue
            #進歩バーの表示
            num = int((i+1)/len(img_URLs)*20)
            bar = "#"*num + " "*(20-num)
            print(bar_template.format(num*5, bar), end="")
        print()
    print("\n保存完了しました")

if __name__ == "__main__":
    main()