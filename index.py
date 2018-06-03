# -*- coding: utf-8 -*-
"""
Created on Thu May 31 09:22:13 2018

@author: David.Bosak
"""

from Functions import convert_pdf_to_txt, preprocess, tokens, word_frequency, downloadPDF



text = convert_pdf_to_txt('document.pdf')
text = preprocess(text)
tokens = tokens(text)
wordfreq = word_frequency(tokens)

from operator import itemgetter
from collections import OrderedDict

sorted_x = OrderedDict(sorted(wordfreq.items(), key=lambda t: t[0]))

d = {'John':5, 'Alex':10, 'Richard': 7}



url = "https://ec.europa.eu/research/participants/data/ref/h2020/other/guide-appl/jti/h2020-guide-techprog-cleansky-ju_en.pdf"
localDestination = "file3.pdf"

downloadPDF(url,localDestination)

text = convert_pdf_to_txt(localDestination)
text = preprocess(text)
token = tokens(text)
wordfreq = word_frequency(token)

