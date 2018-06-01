# -*- coding: utf-8 -*-
"""
Created on Wed May 30 17:24:25 2018

@author: s213984 Alozie Ogechukwu
"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json, re

# Write the fulltext to a txt file
def WriteToFile(title, fulltextlines):
    # Change directory name to local folder where files are to be stored
    directory = r"D:/SEGI_TextAnalytics/Elsevier/ElsevierAPI/FullText/"
    with open(directory + title.replace(':',' -') + ".txt", 'w+', encoding='utf-8') as file:
        file.write(fulltextlines)

## Split the raw text into newlines            
def SplitTextToLines(fulltext):
    fulltextlines = fulltext.replace('. ', '.\n')  
    return fulltextlines
    
   
## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
client.local_dir = r"D:\SEGI_TextAnalytics\Elsevier\ElsevierAPI\SciDirSearch";

## Initialize doc search object and execute search, retrieving all results
doc_srch = ElsSearch('TITLE-ABS-KEY("gas turbine*" AND prognos*) AND ( LIMIT-TO ( SUBJAREA,"ENGI" ) OR LIMIT-TO ( SUBJAREA,"COMP" ) OR LIMIT-TO ( SUBJAREA,"ENER" ) OR LIMIT-TO ( SUBJAREA,"PHYS" ) OR LIMIT-TO ( SUBJAREA,"CENG" ) OR LIMIT-TO ( SUBJAREA,"MATE" ) OR LIMIT-TO ( SUBJAREA,"MATH" ) )','scidir')
# Change get_all = True below to get all results. Beware, might return large count!!!
doc_srch.execute(client, get_all = False)
print ("doc_srch has", len(doc_srch.results), "results.")

## Set up regular expressions for start of abstract and references, and full-stops.
abspatt = re.compile(r'Abstract')
refpatt = re.compile(r'References')
locstart = 0
locend = 0
## Loop through results of document search
for srchresult in doc_srch.results:    
    doi_doc = FullDoc(uri = srchresult['prism:url'])
    if doi_doc.read(client):
        return_data = doi_doc.data
        if (return_data['coredata']['openArchiveArticle'] != False):
            return_title = doi_doc.title
            #return_data = doi_doc.data
            print ("doi_doc.title: ", doi_doc.title)       
            
            # Find matches to abstract, references and full-stop
            absmatch_start = abspatt.finditer(return_data['originalText'])
            for match in absmatch_start:
                locstart = match.start()
                break
            
            refmatch_start = refpatt.finditer(return_data['originalText'])
            for match in refmatch_start:
                locend = match.start()
    
            fulltext = return_data['originalText'][locstart:locend-1]
            
            #fulltextlines = SplitTextToLines(fulltext)
            WriteToFile(return_title, fulltext)
            #doi_doc.write()
        else:
            print("  Not an open source article.")
        
    else:
        print ("Read document failed.")
        