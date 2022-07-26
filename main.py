from lxml import html
import xlsxwriter
import re
import requests

item_links = []
all_items = []


class Item(object):

    def __init__(self, name, url, brand, description, price, currency, image_url, color,
                 quantity, item_type, condition):
        self.name = name
        self.url = url
        self.brand = brand
        self.description = description
        self.price = price
        self.currency = currency
        self.image_url = image_url
        self.color = color
        self.quantity = quantity
        self.item_type = item_type
        self.condition = condition


def initial_request():
    for i in range(1,100):
        try:
            root_url = 'https://www.bonanzamarket.co.uk/items/search?q[country_to_filter]=GB&q[ship_country]' \
                        '=1&q[tas][186873][]=6627596&q[translate_term]=true&q[page]='+str(i)+'&s=6937&q[' \
                        'search_term]=saturn%20ceramic'
            data = requests.get(root_url).content
            path = '//div[2]/div[1]/a'
            source_code = html.fromstring(data)
            tree = source_code.xpath(path)
            for i in tree:
                item_link = i.attrib["href"]
                if item_link[0:9] == "/listings":
                    item_links.append("https://www.bonanzamarket.co.uk/" + item_link)
        except:
            break


def get_item_attributes(link):
    data = requests.get(link).content
    source_code = html.fromstring(data)

    condition = ""
    quantity = ""
    item_type = ""
    color = ""
    brand = ""
    name = source_code.xpath('//meta[@property="og:title"]/@content')[0]
    description = source_code.xpath('//meta[@property="og:description"]/@content')[0]
    price = source_code.xpath('//meta[@property="product:price:amount"]/@content')[0]
    currency = source_code.xpath('//meta[@property="og:price:currency"]/@content')[0]
    image_url = source_code.xpath('//meta[@property="og:image"]/@content')[0]

    table_path = '//div[1]/div[4]/div/div[5]/div[1]/div[1]/div/div[1]/table'
    table1 = source_code.xpath(table_path)[0].text_content()
    text = re.sub("( {2,}\n)|( {2,})", "", table1)
    text_iter = text.splitlines()
    for i in range(len(text_iter)):
        if "Available:" in text_iter[i]:
            quantity = int(re.search(r'\d+', text_iter[i + 1]).group())
            i += 1
        elif "Condition:" in text_iter[i]:
            condition = text_iter[i + 1]
            i += 1
        elif "Type:" in text_iter[i]:
            item_type = text_iter[i + 1]
            i += 1
        elif "Color:" in text_iter[i]:
            color = text_iter[i + 1]
            i += 1
        elif "Brand:" in text_iter[i]:
            brand = text_iter[i + 1]
            i += 1

    all_items.append(Item(name=name, quantity=quantity, item_type=item_type, brand=brand, color=color,
                          description=description, price=price, currency=currency, image_url=image_url))


initial_request()
for item in item_links:
    get_item_attributes(item)
