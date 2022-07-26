from lxml import html
import xlsxwriter
import re
import requests

item_links = []
all_items = []


class Item(object):
    # TODO:: add predefined values for parameters in init
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
    # TODO:: add proper break condition
    for i in range(1,10):
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
    # TODO::add attribute existence checks
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
                          description=description, price=price, currency=currency, image_url=image_url,
                          condition=condition, url=link))
    print(link)


def items_to_xlsx():
    workbook = xlsxwriter.Workbook('C:/Users/Yenip/OneDrive/Belgeler/Excels/demo.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 40)
    worksheet.set_column('G:G', 20)
    worksheet.set_column('J:J', 15)
    worksheet.set_column('K:K', 15)
    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'Name', bold)
    worksheet.write('B1', 'Url', bold)
    worksheet.write('C1', 'Brand', bold)
    worksheet.write('D1', 'Description', bold)
    worksheet.write('E1', 'Price', bold)
    worksheet.write('F1', 'Currency', bold)
    worksheet.write('G1', 'Image url', bold)
    worksheet.write('H1', 'Color', bold)
    worksheet.write('I1', 'Quantity', bold)
    worksheet.write('J1', 'Item type', bold)
    worksheet.write('K1', 'Condition', bold)

    for i in range(0, len(all_items)):
        worksheet.write('A'+str(i+2), all_items[i].name)
        worksheet.write('B'+str(i+2), all_items[i].url)
        worksheet.write('C'+str(i+2), all_items[i].brand)
        worksheet.write('D'+str(i+2), all_items[i].description)
        worksheet.write('E'+str(i+2), all_items[i].price)
        worksheet.write('F'+str(i+2), all_items[i].currency)
        worksheet.write('G'+str(i+2), all_items[i].image_url)
        worksheet.write('H'+str(i+2), all_items[i].color)
        worksheet.write('I'+str(i+2), all_items[i].quantity)
        worksheet.write('J'+str(i+2), all_items[i].item_type)
        worksheet.write('K'+str(i+2), all_items[i].condition)

    workbook.close()


initial_request()
for item in item_links:
    get_item_attributes(item)
items_to_xlsx()



