# -*- coding: utf-8 -*-
"""
Created on Wed May 30 22:39:45 2018

@author: David
"""

#document at https://media.readthedocs.org/pdf/pdfminer-docs/latest/pdfminer-docs.pdf
#pip install pdfminer.six


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
# Open a PDF document.
fp = open('document1.pdf', 'rb')
parser = PDFParser(fp)
document = PDFDocument(parser, '')
# Get the outlines of the document.
outlines = document.get_outlines()
for (level,title,dest,a,se) in outlines:
    print (level, title)