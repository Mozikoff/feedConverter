from xml.etree import ElementTree
import csv

def fromXmlToCsv():
    tree = ElementTree.parse('C:\\Users\\emozikov\\PycharmProjects\\feedConverter\\yandex_730539_k50-2-win1251-series_09_18.php.xml')
    f = open('test.csv', 'w', newline='', encoding='cp1251')
    csvwriter = csv.writer(f, delimiter=';')

    col_names = ['offer_id', 'url', 'price', 'categoryId', 'picture', 'name']
    csvwriter.writerow(col_names)

    root = tree.getroot()
    for offer in root.iter('offer'):
        data = []
        data.append(offer.attrib['id'])
        data.append(offer.find('url').text)
        data.append(offer.find('price').text)
        data.append(offer.find('categoryId').text)
        data.append(offer.find('picture').text)
        data.append(offer.find('name').text)
        csvwriter.writerow(data)

    f.close()


if __name__ == '__main__':
    fromXmlToCsv()