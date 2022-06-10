import pandas as pd

from lxml import html

import requests as requests


def get_detail(name):
    if name == "":
        return "nil", "nil", "nil", "nil"
    # 在下面的代码行中使用断点来调试脚本。
    tmp_url = "https:" + name
    http_response = requests.get(tmp_url)
    http_response.encoding = 'gbk'
    response_text = http_response.text
    selector = html.etree.HTML(response_text)
    img_text = selector.xpath('//*[@id="showSkin"]/div/img/@src')[0]
    skin_text = selector.xpath('//*[@id="showSkin"]/div/div[2]/span[1]/text()')[0]
    hero_selector = selector.xpath('//*[@id="showSkin"]/div/div[2]/span[2]/text()')
    if len(hero_selector) < 1:
        return img_text, skin_text, "nil", response_text
    hero_text = hero_selector[0]
    skin_desc_text = selector.xpath('//*[@id="showSkin"]/div/p/text()')[0]
    return img_text, skin_text, hero_text, skin_desc_text


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    url = "https://pvp.qq.com/zlkdatasys/data_zlk_xpflby.json"
    response = requests.get(url).json()
    datas = []
    for i in response['pcblzlby_c6']:
        img_text, skin_text, hero_text, skin_desc_text = get_detail(str(i['pcblzlbyxqydz_c4']))
        if hero_text != "nil":
            data = {
                "皮肤名称": skin_text,
                "英雄名称": hero_text,
                "皮肤描述": skin_desc_text,
                "皮肤图像": img_text
            }
            datas.append(data)

    headers = ['皮肤名称', '英雄名称', '皮肤描述', '皮肤图像']

    df = pd.DataFrame(datas, columns=headers)
    df.to_csv("csv_皮肤.tsv",header=headers, sep="\t")
