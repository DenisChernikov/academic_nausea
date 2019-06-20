#!/usr/bin/env python3
# coding: utf8

import re
import pymorphy2
from stop_phrases import stop_phrases
from collections import Counter


def nausea(article):
    if not isinstance(article, str):
        raise AssertionError('Переданное значение не является строкой')
    article = article.lower()

    def words_list(text):
        return tuple(re.findall(r'([а-яё\'-]+)', text))

    words = words_list(article)
    total_words = len(words)

    for i in stop_phrases:
        article = article.replace(i, '')

    words = words_list(article)
    counter = Counter(words)

    morph = pymorphy2.MorphAnalyzer()

    result = {}
    for k in list(counter.keys()):
        p = morph.parse(k)[0]

        # Удаляем предлоги, союзы, частицы, междометия, наречия, местоимения, предикативы, числительные, компаративы
        if p.tag.POS in ['PREP', 'CONJ', 'PRCL', 'INTJ', 'ADVB', 'NPRO', 'PRED', 'NUMR', 'COMP']:
            del counter[k]
        else:
            group = result.setdefault(p.normal_form, [0, []])
            group[0] += counter[k]
            group[1].append(k)

    result = sorted(result.items(), key=lambda kv: kv[1][0])

    most_used = result[-1][1][0]
    nausea = most_used / total_words
    result_words = None
    if nausea > 0.09:
        result_words = []
        for i in reversed(result):
            if i[1][0] == most_used:
                for j in i[1][1]:
                    result_words.append(j)
            else:
                break
    return nausea, result_words
