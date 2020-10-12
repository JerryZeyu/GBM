from lxml import etree
import argparse
import random
import spacy
import glob
import re
import os
import sys

#filter the description in which the fist sentence or second sentence contain the word "centry"
#filter the description in which the entity text's first letter is not capital
def text_based_conditions(data_entity, entity_name, nlp):
    text = " ".join(data_entity.xpath('./p/text()'))
    document = nlp(text)
    entity_name_splits = re.split("_|,|,_", entity_name)
    entity_flag = 0
    for entity_name_split in entity_name_splits:
        if entity_name_split in text:
            entity_flag = 1
    century_flag = 0
    for sent in list(document.sents)[0:2]:
        if 'century' in sent.string:
            century_flag = 1
    return entity_flag == 1 and century_flag == 0


def get_entities_fromCollections(collections_dir):

    text_filepath = os.path.join(collections_dir, 'GLCollection.xml')
    collection = etree.parse(text_filepath)
    all_entities = collection.xpath('//entity')
    return all_entities

def extract_save_entities(sample_entities, output_dir, collections_dir, nlp):
    sample_doc = etree.Element('data', id='GLSample')
    sample_entities_xml = etree.SubElement(sample_doc, 'entities')
    for sample_entity in sample_entities:
        entity_id = sample_entity.get("entity_id")
        data_id = sample_entity.get("data_id")
        data = etree.parse(os.path.join(collections_dir, data_id))
        data_entity = data.xpath('//entity[@id="' + entity_id + '"]')[0]
        entity_type = data_entity.get("type")
        entity_name = data_entity.get("wikipedia")
        if ("relation" in entity_type or "way" in entity_type) and text_based_conditions(data_entity, entity_name, nlp):
            title_flag = 0
            for p in data_entity.xpath('./p'):
                pid = p.get("id")
                for e, link in enumerate(p.xpath('./link')):
                    linkid = "%s_%03d" % (pid, e + 1)
                    link.set("id", linkid)
                    if not link.text.istitle():
                        title_flag = 1
            data_entity.set("status", "5")
            if title_flag == 0:
                sample_entities_xml.append(data_entity)

    sample_tree = etree.ElementTree(sample_doc)
    with open(os.path.join(output_dir, 'train_samples.xml'), 'wb') as sample_file:
        sample_tree.write(sample_file, xml_declaration=True, encoding='utf-8')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--collections_dir', default='../geocode-data/collection', type=str,
                        help='path of data collections')
    parser.add_argument('--sample_size', default=50, type=int,
                        help='number of sample datas')
    parser.add_argument('--output_dir', default='../geocode-data/collection_samples', type=str,
                        help='path of data collections samples')
    args = parser.parse_args()
    nlp = spacy.load("en_core_web_sm")
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    all_entities = get_entities_fromCollections(args.collections_dir)
    sample_entities = random.sample(all_entities, args.sample_size)
    extract_save_entities(sample_entities, args.output_dir, args.collections_dir, nlp)
