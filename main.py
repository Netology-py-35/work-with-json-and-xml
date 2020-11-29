#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

import xml.etree.ElementTree as ET


def get_xml_bag_of_words(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    news_xml = root.findall('channel/item')
    news_list = []
    for news in news_xml:
        news_list.extend(news.find('description').text.split(' '))
    return news_list


def get_json_bag_of_words(json_file):
    with open(json_file, 'r') as file:
        news = json.loads(file.read())
    word_items = news['rss']['channel']['items']
    bag_of_words = []
    for item in word_items:
        bag_of_words.extend(item['description'].split(' '))
    return bag_of_words


def word_count(words, min_lenth:int):
    counts = {}
    for word in words:
        if len(word) > min_lenth:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
    return counts


def print_top_words(words, top_index:int, min_lenth:int):
    s = sorted(word_count(words, min_lenth).items(), key=lambda item: item[1])
    s.reverse()
    for word in s[:top_index]:
        print(f'слово "{word[0]}" встречается {word[1]} раз')


if __name__ == '__main__':
    json_file = './newsafr.json'
    xml_file = './newsafr.xml'

    words = {'json': get_json_bag_of_words(json_file), 'xml': get_xml_bag_of_words(xml_file)}

    for w in words.items():
        print(f'ТОП 10 слов в файле {w[0]}')
        print_top_words(w[1], 10, 6)
        print()
