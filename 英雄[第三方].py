import csv
from lxml import html
import requests as requests

import pandas as pd


def get_detail(name):
    list_data = []
    # 在下面的代码行中使用断点来调试脚本。
    tmp_url = "https://db.18183.com" + name
    http_response = requests.get(tmp_url)
    response_text = http_response.text
    selector = html.etree.HTML(response_text)
    hero_name = selector.xpath('//div[@class="name-box"]/h1/text()')[0]
    list_data.append(hero_name)
    basic_type = selector.xpath('//div[@class="hero-basicinfo-box fl"]/div[@class="base"]/dl/dd/text()')[0].strip()
    list_data.append(basic_type)
    basic_data_li = selector.xpath('//div[@class="otherinfo-datapanel"]/ul/li')
    for li in basic_data_li:
        pdata_str = li.xpath("./p/text()")[0]
        pdata = pdata_str.split("：")
        list_data.append(pdata[1].replace('%', ''))
    return list_data


def get_data():
    url = "https://db.18183.com/wzry/"
    http_response = requests.get(url)
    response_text = http_response.text
    selector = html.etree.HTML(response_text)

    div_people_li = selector.xpath("//ul[@class='mod-iconlist']/li")

    datas = []

    headers = ["英雄名称", "英雄类型",
               '最大生命', '最大法力', '物理攻击', '法术攻击', '物理防御', '物理减伤率', '法术防御', '法术减伤率', '移速',
               '物理护甲穿透', '法术护甲穿透', '攻速加成', '暴击几率',
               '暴击效果', '物理吸血', '法术吸血', '冷却缩减', '攻击范围', '韧性', '生命回复', '法力回复']

    for i in div_people_li:
        item_href = i.xpath('./a/@href')
        list_data = get_detail(
            str(item_href[0]))
        datas.append(list_data)

    df = pd.DataFrame(datas, columns=headers);
    data = df.drop_duplicates(subset=['英雄名称'], keep='first', inplace=False)
    data.to_csv("csv_英雄.tsv", index=False, sep="\t")


def handle_data():
    # data
    get_data()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    handle_data()
