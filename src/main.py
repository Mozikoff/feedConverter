from xml.etree import ElementTree
import csv
import requests
import sys
import time


def from_xml_to_csv(url):
    root = ElementTree.fromstring(requests.get(url).content)
    file_name = url.rsplit('/', 1)[1].split('.')[0] + str(time.time()) + '.csv'
    f = open(file_name, 'w', newline='', encoding='cp1251')
    csvwriter = csv.writer(f, delimiter=';')

    col_names = ['id', 'group id', 'available', 'typePrefix', 'vendor', 'model', 'name', 'category', 'price',
                 'oldprice', 'currencyId', 'url', 'vendorcode', 'picture', 'description', 'country_of_origin',
                 'manufacturer_warranty', 'sales_notes', 'pickup', 'store', 'delivery', 'barcode', 'adult']
    csvwriter.writerow(col_names)

    for offer in root.iter('offer'):
        data = []
        data.append(offer.attrib.get('id'))
        data.append(offer.attrib.get('group_id'))
        data.append(offer.attrib.get('available', 'true'))
        data.append(offer.findtext('typePrefix'))
        data.append(offer.findtext('vendor'))
        data.append(offer.findtext('model'))
        data.append(offer.findtext('name'))
        category_path = get_category_path(root, offer.findtext('categoryId'))
        data.append(category_path)
        data.append(offer.findtext('price'))
        data.append(offer.findtext('oldprice'))
        data.append(offer.findtext('currencyId'))
        data.append(offer.findtext('url'))
        data.append(offer.findtext('vendorCode'))
        data.append(offer.findtext('picture'))    #TODO: many
        data.append(offer.findtext('description'))
        data.append(offer.findtext('country_of_origin'))
        data.append(offer.findtext('manufacturer_warranty'))
        data.append(offer.findtext('sales_notes'))
        data.append(offer.findtext('pickup'))
        data.append(offer.findtext('store'))
        data.append(offer.findtext('delivery'))    #TODO: options
        data.append(offer.findtext('barcode'))
        data.append(offer.findtext('adult'))
        data.append(offer.findtext('adult'))
        #TODO: params

        csvwriter.writerow(data)

    f.close()


def get_category_path(root, category):
    cat = root.find(f'.//category[@id="{category}"]')
    path = f'(id:{cat.attrib["id"]}){cat.text}'
    parent = cat.attrib.get('parentId')
    while parent:
        cat = root.find(f'.//category[@id="{parent}"]')
        path = f'(id:{cat.attrib["id"]}){cat.text}|' + path
        parent = cat.attrib.get('parentId')
    return path


def main():
    url = sys.argv[1]
    print(url)
    from_xml_to_csv(url)
    print('Completed!')


if __name__ == '__main__':
    main()
