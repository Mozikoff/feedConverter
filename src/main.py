from xml.etree import ElementTree
import csv
import requests
import sys
import time


def from_xml_to_csv(url):
    root = ElementTree.fromstring(requests.get(url).content)
    file_name = url.rsplit('/', 1)[1].split('.')[0] + '_' + str(time.time()) + '.csv'
    f = open('reports/' + file_name, 'w', newline='', encoding='utf-8-sig')
    csvwriter = csv.writer(f, delimiter=';', dialect='excel')

    if root.tag == 'yml_catalog':
        parse_yml(root, csvwriter)
    else:
        parse_gml(root, csvwriter)

    f.close()


def parse_yml(root, csvwriter):
    col_names = ['id', 'group id', 'available', 'typePrefix', 'vendor', 'model', 'name', 'category', 'price',
                 'oldprice', 'currencyId', 'url', 'vendorcode', 'picture', 'description', 'country_of_origin',
                 'manufacturer_warranty', 'sales_notes', 'pickup', 'store', 'delivery', 'barcode', 'adult', 'bid',
                 'condition-type', 'condition-reason', 'credit-template-id', 'dimensions', 'expiry', 'weight']
    update_yml_col_names_with_params(root, col_names)
    csvwriter.writerow(col_names)

    for offer in root.iter('offer'):
        data = dict.fromkeys(col_names)
        data['id'] = offer.attrib.get('id')
        data['group_id'] = offer.attrib.get('group_id')
        data['available'] = offer.attrib.get('available', 'true')
        data['typePrefix'] = offer.findtext('typePrefix')
        data['vendor'] = offer.findtext('vendor')
        data['model'] = offer.findtext('model')
        data['name'] = offer.findtext('name')
        data['category'] = get_category_path(root, offer.findtext('categoryId'))
        data['price'] = offer.findtext('price')
        data['oldprice'] = offer.findtext('oldprice')
        data['currencyId'] = offer.findtext('currencyId')
        data['url'] = offer.findtext('url')
        data['vendorcode'] = offer.findtext('vendorCode')
        data['picture'] = get_offer_pictures(offer)
        data['description'] = offer.findtext('description', "").replace("\n", "|")
        data['country_of_origin'] = offer.findtext('country_of_origin')
        data['manufacturer_warranty'] = offer.findtext('manufacturer_warranty')
        data['sales_notes'] = offer.findtext('sales_notes')
        data['pickup'] = offer.findtext('pickup')
        data['store'] = offer.findtext('store')
        data['delivery'] = offer.findtext('delivery')
        data['barcode'] = offer.findtext('barcode')
        data['adult'] = offer.findtext('adult')
        data['bid'] = offer.attrib.get('bid')
        cond = offer.find('condition')
        condition_type = cond.attrib.get('type') if cond is not None else ''
        data['condition-type'] = condition_type
        data['condition-reason'] = offer.findtext('condition/reason')
        credit_template = offer.find('credit-template')
        temp = credit_template.attrib.get('id') if credit_template is not None else ''
        data['credit-template-id'] = temp
        data['dimensions'] = offer.findtext('dimensions', "").replace("\n", "|")
        data['expiry'] = offer.findtext('expiry')
        data['weight'] = offer.findtext('weight')
        for param in offer.iter('param'):
            field_name = param.attrib.get('name') if param.attrib.get('unit') is None \
                else param.attrib.get('name') + str(param.attrib.get('unit'))
            data[field_name] = param.text.replace("\n", "|")

        csvwriter.writerow(data.values())


def parse_gml(root, csvwriter):
    col_names = []
    update_gml_col_names(root, csvwriter, col_names)
    for item in root.findall('./channel/item'):
        data = dict.fromkeys(col_names)
        for elem in item.iterfind('./*'):
            elem_name = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
            data[elem_name] = elem.text.replace("\n", "|")
        csvwriter.writerow(data.values())


def update_yml_col_names_with_params(root, col_names):
    for offer in root.iter('offer'):
        for param in offer.iter('param'):
            field_name = param.attrib.get('name') if param.attrib.get('unit') is None \
                else param.attrib.get('name') + str(param.attrib.get('unit'))
            if field_name not in col_names:
                col_names.append(field_name)


def update_gml_col_names(root, csvwriter, col_names):
    for item in root.findall('./channel/item'):
        for elem in item.iterfind('./*'):
            elem_name = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
            if elem_name not in col_names:
                col_names.append(elem_name)
    csvwriter.writerow(col_names)



def get_offer_pictures(offer):
    pic = set()
    for picture in offer.iter('picture'):
        pic.add(picture.text)
    return ','.join(pic)


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
