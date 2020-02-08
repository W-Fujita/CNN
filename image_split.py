from scrape import search_word
import os
import glob
import random
import shutil

os.makedirs("./Train", exist_ok=True) #トレーニングデータの画像用フォルダ
os.makedirs("./Test", exist_ok=True) #テストデータの画像用フォルダ

for word in search_word:
    print("{}の画像を分割します".format(word))
    input_dir = "./Edited/"+word+"/*"
    img_list = glob.glob(input_dir)
    random.shuffle(img_list) #img_listの要素をランダムにソート
    os.makedirs("./Train/"+word, exist_ok=True) #フォルダの作成
    os.makedirs("./Test/"+word, exist_ok=True)

    #img_listの2割をテスト用に保存
    for i in range(len(img_list)):
        if i < len(img_list)/5:
            shutil.copy2(str(img_list[i]), "./Test/"+word)
        else:
            shutil.copy2(str(img_list[i]), "./Train/"+word)

print("分割を終了しました")