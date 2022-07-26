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

    price_path = '//div[1]/div[4]/div/div[2]/div[1]'
    res = source_code.xpath(price_path)[0].text_content()
    price = re.search("(.\d+\.\d\d)", res).group()

    table_path = '//div[1]/div[4]/div/div[5]/div[1]/div[1]/div/div[1]/table'
    table1 = source_code.xpath(table_path)[0].text_content()
    text = re.sub("( {2,}\n)|( {2,})", "", table1)
    text_iter = text.splitlines()
    for i in range(len(text_iter)):
        if "Available:" in text_iter[i]:
            quantity = int(re.search(r'\d+', text_iter[i+1]).group())
            i += 1
        elif "Condition:" in text_iter[i]:
            condition = text_iter[i+1]
            i += 1
        elif "Type:" in text_iter[i]:
            item_type = text_iter[i+1]
            i += 1
        elif "Color:" in text_iter[i]:
            color = text_iter[i+1]
            i += 1
        elif "Brand:" in text_iter[i]:
            brand = text_iter[i+1]
            i += 1

    print(price, name, brand)



# for link in item_links:
#     get_item_attributes(link)

r = http.request('GET', "https://www.bonanzamarket.co.uk//listings/Saturn-Ceramic-Gilding-Pattern-Modern-Handmade-Special-Design-Ceramic-Flowerpot/1306985327")
data_string = r.data.decode('utf-8', errors='ignore')
source_code = html.fromstring(data_string)
#print(source_code.text_content())

desc_path = '//*[@id="content"]/div[1]/div[4]/div/div[6]/div[2]/div[3]'
xxx = data_string
print(source_code.xpath(desc_path)[0])
#get_item_attributes(item_links[0])
