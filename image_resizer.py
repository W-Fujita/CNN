from scrape import search_word #"dog","cat"
import glob
import os
import cv2

for word in search_word:
    print("{}の画像を加工します".format(word))
    input_dir = "./Original/"+word+"/*"
    img_list = glob.glob(input_dir)
    output_dir = "./Edited/"+word
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(len(img_list)):
        img = cv2.imread(str(img_list[i]))
        if img is None:
             print("image{}:NoImage".format(str(i)))
        else:
            img = cv2.resize(img, (250,250)) #画像のサイズ変更
            path = os.path.join(output_dir, str(i)+".jpg")
            cv2.imwrite(str(path), img)

print("加工を終了しました")