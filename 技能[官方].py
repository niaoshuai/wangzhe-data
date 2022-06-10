import csv

from lxml import html

import requests as requests


def get_detail(name):
    if name == "":
        return "nil", "nil", "nil", "nil"
    # 在下面的代码行中使用断点来调试脚本。
    tmp_url = "https://pvp.qq.com/web201605/" + name
    http_response = requests.get(tmp_url)
    http_response.encoding = 'gbk'
    response_text = http_response.text
    selector = html.etree.HTML(response_text)
    hero_name = selector.xpath('//h2[@class="cover-name"]/text()')[0]
    skill_name_p = selector.xpath('//p[@class="skill-name"]')
    skill_name0 = skill_name_p[0].xpath("b/text()")[0]
    skill_name1 = skill_name_p[1].xpath("b/text()")[0]
    skill_name2 = skill_name_p[2].xpath("b/text()")[0]
    skill_name3 = skill_name_p[3].xpath("b/text()")[0]
    skill_name4 = ""
    if len(skill_name_p[4].xpath("b/text()")) > 0:
        skill_name4 = skill_name_p[4].xpath("b/text()")[0]
    return hero_name, skill_name0, skill_name1, skill_name2, skill_name3, skill_name4


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    url = "https://pvp.qq.com/web201605/herolist.shtml"
    http_response = requests.get(url)
    http_response.encoding = 'gbk'
    response_text = http_response.text
    selector = html.etree.HTML(response_text)

    div_people_li = selector.xpath("//ul[@class='herolist clearfix']/li")

    # csv 写入
    f = open('csv_技能.csv', 'w', encoding='utf-8')
    csv_write = csv.writer(f)
    csv_write.writerow(['英雄', '被动', '技能1', '技能2', '技能3', '技能4'])

    for i in div_people_li:
        item_href = i.xpath('./a/@href')
        hero_name, skill_name0, skill_name1, skill_name2, skill_name3, skill_name4 = get_detail(
            str(item_href[0]))
        csv_write.writerow([hero_name, skill_name0, skill_name1, skill_name2, skill_name3, skill_name4])

    f.close()
