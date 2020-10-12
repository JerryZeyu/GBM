from lxml import etree
import random
import re
import os
import sys

def text_based_conditions(data_entity):
    text = " ".join(data_entity.xpath('./p/text()'))
    max_c_ord = max([ord(c) for c in re.sub(r'^[^\)]+\)','', text)])
    return max_c_ord <= 160


outdir = '../geocode-data/collection'
sample_size = 10

sample_doc = etree.Element('data', id='GLSample')
sample_entities = etree.SubElement(sample_doc, 'entities')
collection = etree.parse(os.path.join(outdir, "GLCollection.xml"))
entities = collection.xpath('//entity')
random.shuffle(entities)
i = 0
while i < sample_size:
    sample_entity = entities[0]
    entities = entities[1:]
    print(sample_entity)
    entity_id = sample_entity.get("entity_id")
    print('entity id: ', entity_id)
    data_id = sample_entity.get("data_id")
    print('data id: ', data_id)
    data = etree.parse(os.path.join(outdir, data_id))
    data_entity = data.xpath('//entity[@id="' + entity_id + '"]')[0]
    entity_type = data_entity.get("type")
    if ("relation" in entity_type or "way" in entity_type) and text_based_conditions(data_entity):
        for p in data_entity.xpath('./p'):
            pid = p.get("id")
            for e, link in enumerate(p.xpath('./link')):
                linkid = "%s_%03d" % (pid, e+1)
                link.set("id", linkid)
        data_entity.set("status", "0")
        sample_entities.append(data_entity)
        print(i)
        i += 1

sample_tree = etree.ElementTree(sample_doc)
# with open(sys.argv[3], 'wb') as sample_file:
#     sample_tree.write(sample_file, xml_declaration=True, encoding='utf-8')

