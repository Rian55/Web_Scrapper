import urllib3
from lxml import html
import xlsxwriter
import re

http = urllib3.PoolManager()
item_links = []


def initial_request():
    r = http.request('GET', 'https://www.bonanzamarket.co.uk/items/search?q[country_to_filter]=GB&q['
                            'ship_country]=1&q[tas][186873][]=6627596&q[translate_term]=true&q[page]=3&s=6937&q['
                            'search_term]=saturn%20ceramic')
    data_string = r.data.decode('utf-8', errors='ignore')
    path = '//div[2]/div[1]/a'
    source_code = html.fromstring(data_string)
    tree = source_code.xpath(path)
    for i in tree:
        item_link = i.attrib["href"]
        if item_link[0:9] == "/listings":
            item_links.append("https://www.bonanzamarket.co.uk/" + item_link)


initial_request()

def get_item_attributes(link):
    name = ""
    description = ""
    price = ""
    item_type = ""
    color = ""
    brand = ""
    condition = ""
    quantity = 0

    r = http.request('GET', link)
    data_string = r.data.decode('utf-8', errors='ignore')
    source_code = html.fromstring(data_string)

    name_path = '//*[@id="content"]/div[1]/div[4]/div/div[2]/div[1]/h2/span'
    name = source_code.xpath(name_path)[0].text_content()

    #description_path = '//*[@id="content"]/div[1]/div[4]/div/div[2]/div[1]/h2/span'
    #description = source_code.xpath(description_path)[0].text_content()

    print(name, " ", link, " ", description)
    price_path = '//div[1]/div[4]/div/div[2]/div[1]'
    res = source_code.xpath(price_path)[0].text_content()
    x = re.search("(.\d+\.\d\d)", res)
    price = x.group()

    table1_path = '//div[1]/div[4]/div/div[5]/div[1]/div[1]/div/div[1]/table'
    table1 = source_code.xpath(table1_path)[0].text_content()
    print(table1)

    color_path = '//*[@id="content"]/div[1]/div[4]/div/div[5]/div[1]/div[1]/div/div[1]/table/tbody/tr[6]/td/p'
    color = source_code.xpath(color_path)[0].text_content()

    brand_path = '//*[@id="content"]/div[1]/div[4]/div/div[5]/div[1]/div[1]/div/div[1]/table/tbody/tr[8]/td/p/span'
    brand = source_code.xpath(brand_path)[0].text_content()

    condition_path = '//*[@id="content"]/div[1]/div[4]/div/div[5]/div[1]/div[1]/div/div[1]/table/tbody/tr[3]/td/p/text()'
    condition = source_code.xpath(condition_path)[0].text_content()


# for link in item_links:
#     get_item_attributes(link)

r = http.request('GET', "https://www.bonanzamarket.co.uk//listings/Saturn-Ceramic-Gilding-Pattern-Modern-Handmade-Special-Design-Ceramic-Flowerpot/1306985327")
data_string = r.data.decode('utf-8', errors='ignore')
source_code = html.fromstring(data_string)


get_item_attributes(item_links[0])
