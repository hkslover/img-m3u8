import requests
import os
import json
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
url = 'https://cdn-ms.juejin.im/v1/upload?bucket=gold-user-assets'
def replace_m3u8(list1):
    f = open('index.m3u8','r', encoding='utf-8')
    str1 = f.read()
    for x in list1:
        str1 = str1.replace(x[0].split('.')[0] + '.ts',x[1])
    ff = open('new_index.m3u8','w')
    ff.write(str1)
    ff.close()
    f.close()
    os.system('del index.m3u8')
    os.system('del *.png')
def upload():
    data_list = []
    path_list = os.listdir(os.getcwd())
    for x in path_list:
        if os.path.splitext(x)[1] == '.png': 
            files = {'file': open(x, 'rb')}
            response = requests.post(url,headers = headers,files = files)
            json_data = json.loads(response.text)
            return_url = json_data['d']['url']['http']
            print(return_url)
            data_list.append((x,return_url))
    print(data_list)
    replace_m3u8(data_list)
def split_ts(file_path):
    os.system('ffmpeg -i ' + file_path + ' -c copy -map 0 -f segment -segment_list index.m3u8 -segment_time 1 output%03d.ts')
    os.system('ren *.ts *.png')
    upload()
if __name__ == "__main__":
    video = input('Video File:')
    split_ts(video)