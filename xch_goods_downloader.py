import json
import os
import requests
import pymysql
import time
import random
#连接数据库
db = pymysql.connect(
        host='192.168.0.10',
        port= 3306,
        user='xchgoods',
        passwd='WkeCt5sY57iY5nat',
        db='xchgoods',
        charset='utf8'
)
cur = db.cursor()
#请求头部
head = {
"Content-Type": "application/json;charset=UTF-8",
"imei": "867254034274675",
"oaid":"",
"type":"5",
"Host": "api.替换.com",
"Connection": "keep-alive",
"vary": "accept-encoding",
"Accept-Encoding": "gzip",
"Set-Cookie": "SERVERID=c4bf6b715c0f1b68d7933c2b67e75c86|1608444064|1608444059;Path=/",
"User-Agent": "okhttp/3.12.0",
}
head2 = {
"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; unknown Build/LMY48Z)",
"Connection": "Keep-Alive",
"Accept-Encoding": "gzip",
}
#根据品牌id，创建文件夹并进入
with open("d:\\project\\data\\goods_id.txt",'r') as f:
    for line in f.read().splitlines():
        dir = 'd:\\project\\download\\' + line + '\\'
        print(dir)
        if os.path.exists(dir):
            os.chdir(dir)
        else:
            os.makedirs(dir)
            os.chdir(dir)
#根据品牌id，构造url，并获取对应json
        url = "https://api.替换.com/api/goods/detail?id="
        url_new = url + line
        #随机休眠5秒
        sleeptime = random.randint(0, 5)
        time.sleep(sleeptime)
        get_info = requests.get(url_new,headers=head).content
        read_info = json.loads(get_info)
#读取获取商品详情信息
        brands_id = read_info['data']['brand']['id']
        brands_name = read_info['data']['brand']['name']
        brands_name_en = read_info['data']['brand']['englishName']
        goods_id = read_info['data']['info']['id']
        goods_brief = read_info['data']['info']['brief']
        goods_category_id = read_info['data']['info']['categoryId']
        goods_keywords = read_info['data']['info']['keywords']
        market_price = read_info['data']['info']['counterPrice']
        retail_price = read_info['data']['info']['retailPrice']
        vip_price = read_info['data']['info']['vipPrice']
        pic = read_info['data']['info']['picUrl']
        main_pic = str(pic).replace("?x-oss-process=style/sy","\n")
        main_video = read_info['data']['info']['videoUrl']
        add_time = read_info['data']['info']['addTime']
        update_time = read_info['data']['info']['updateTime']
#替换图库部分的特殊字符
        gallery = read_info['data']['info']['gallery']
        goods_gallery = str(gallery).replace('[','').replace(']','').replace("'","").replace(", ","\n").replace("?x-oss-process=style/sy","")
#写入数据库
        sql_values = (brands_id,brands_name,brands_name_en,goods_id,goods_brief,goods_category_id,goods_keywords,market_price,retail_price,vip_price,main_pic,main_video,add_time,update_time,goods_gallery)
        sql = "Insert into goods_detail(brands_id,brands_name,brands_name_en,goods_id,goods_brief,goods_category_id,goods_keywords,market_price,retail_price,vip_price,main_pic,main_video,add_time,update_time,goods_gallery) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql,sql_values)
        db.commit()
#下载图片到本地
        with open('d:\\project\\download\\tempurl.txt','wb') as i:
            i.write(main_pic.encode())
            i.write(goods_gallery.encode())
            i.close()
        with open("d:\\project\\download\\tempurl.txt",'r') as j:
            for line in j.read().splitlines():
                    time.sleep(2)
                    i_url = requests.get(line,headers=head2)
                    filename = line.split("/")[-1]
                    with open(filename,'wb') as k:
                        k.write(i_url.content)
        j.close()
        os.remove('d:\\project\\download\\tempurl.txt')
        os.chdir('d:\\project\\download\\')
        print(goods_id,"done")
print("全部下载完成")
