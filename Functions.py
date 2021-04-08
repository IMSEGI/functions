# -*- coding: utf-8 -*-
"""
Created on Thu May 31 08:52:52 2018

@author: David.Bosak
"""


##############################################
# convert PDF to text
import io
import nltk
import string

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

##############################################
#Removing Punctuation and Stop Words nltk
import string
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re

def preprocess(sentence):
    sentence = sentence.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(sentence)
    filtered_words = [w for w in tokens if not w in stopwords.words('english')]
    return " ".join(filtered_words)

##############################################
#extract tokens from sentence
from nltk.tokenize import RegexpTokenizer

def tokens(sentence):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(sentence)
    return tokens

##############################################
#extract word frequency
from nltk import FreqDist
import nltk

def word_frequency(tokens):
    fdist = FreqDist(tokens)
    return fdist


#############################################
# download PDFs from intenet and save in local directory
# https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
import urllib.request

def downloadPDF(url,localDestination):
    urllib.request.urlretrieve(url, localDestination)
    

#############################################
# execute cURL command in python
# https://curl.trillworks.com/
# http://documents.epo.org/projects/babylon/eponet.nsf/0/F3ECDCC915C9BCD8C1258060003AA712/$File/ops_v3.2_documentation_-_version_1.3.6_en.pdf
    
import epo_ops


client = epo_ops.Client(key='C8o2GsPsNfsXtVLRTj2vwSKObWCQsFZ1', secret='q0M6AJJ4NO1lV9CY')  # Instantiate client
response = client.published_data(  # Retrieve bibliography data
  reference_type = 'publication',  # publication, application, priority
  input = epo_ops.models.Docdb('2587024', 'EP', 'A2'),  # original, docdb, epodoc
  endpoint = 'abstract',  # optional, defaults to biblio in case of published_data
  constituents = []  # optional, list of constituents
)
