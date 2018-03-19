# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from __future__ import division
import numpy as np
import pandas as pd
import json
from pymystem3 import Mystem
import regex as re

analyzer = Mystem()
strip_characters = '!`«»‰~@\'▲▼„"#$%^&*()_-+=[]\{\}°:;|•.,<>?/————–'
split_reg = re.compile('[\s\(\)\.,;"«»\'\[\]&<>]+')
punctuation = set(strip_characters)
# num_reg = re.compile(r'[0-9)(:\-/№#]+?')

with open('stop_words.json') as file:
        stop_words = json.load(file)

def tokenize(string, need_pos=False):
    tokens = [lemmatize_pos_tag(i.lower().strip(strip_characters), need_pos=need_pos) 
                  for i in re.split(split_reg, string) if i.strip(strip_characters) and i not in punctuation 
                  and i not in stop_words]
    valid_tokens = []
    for token in tokens:
        if token:
            valid_tokens.append(token)
    return valid_tokens

def lemmatize_pos_tag(token, need_pos):
    if need_pos:
        analysis = analyzer.analyze(token)
        try:
            lemma = analysis[0]['analysis'][0]['lex']
            pre_pos = re.split('[,=]+?', analysis[0]['analysis'][0]['gr'])[0]
            pos = pos_map[pre_pos]
            lemma = lemma+'_'+pos
        except (KeyError, IndexError) as e:
            lemma = token
            pos = 'NOUN'
            lemma = lemma+'_'+pos
    else:
        try:
            lemma = analyzer.lemmatize(token)[0]
        except (KeyError, IndexError) as e:
            lemma = token
    return lemma

def sentence_split(text):
    # не state-of-art, но для данного случая подойдет
    abbr = re.compile('(?:\s|^)((?:[а-яё]{1,3}\.)*[а-яё]{1,3}\.)', flags=re.I)
    for substr in re.findall(abbr, text):
        text = text.replace(substr, substr.replace('.', '<dot>'))
    sentences = re.split('[!?;\.]+', text)
    for i in range(len(sentences)):
        sentences[i] = sentences[i].replace('<dot>', '.')
    return sentences