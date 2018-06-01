# -*- coding: utf-8 -*-
"""
Created on Wed May 30 14:34:06 2018

@author: s213984 Alozie Ogechukwu
"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json

def WriteToFile(title, abstract):
    # Change directory name to local folder where files are to be stored
    directory = r"D:/SEGI_TextAnalytics/Elsevier/ElsevierAPI/Abstract/"
    with open(directory + title.replace(':','_') + ".txt", 'w+') as file:
        file.write(abstract)
    
   
## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
client.local_dir = r"D:\SEGI_TextAnalytics\Elsevier\ElsevierAPI\ScopusSearch";

## Initialize doc search object and execute search, retrieving all results
doc_srch = ElsSearch('TITLE-ABS-KEY("gas turbine*" AND prognos*) AND ( LIMIT-TO ( SUBJAREA,"ENGI" ) OR LIMIT-TO ( SUBJAREA,"COMP" ) OR LIMIT-TO ( SUBJAREA,"ENER" ) OR LIMIT-TO ( SUBJAREA,"PHYS" ) OR LIMIT-TO ( SUBJAREA,"CENG" ) OR LIMIT-TO ( SUBJAREA,"MATE" ) OR LIMIT-TO ( SUBJAREA,"MATH" ) )','scopus')
# Change get_all = True below to get all results. Beware, might return large count!!!
doc_srch.execute(client, get_all = False)   
print ("doc_srch has", len(doc_srch.results), "results.")

## Loop through results of document search
for srchresult in doc_srch.results:    
    scp_doc = AbsDoc(uri = srchresult['prism:url'])
    if scp_doc.read(client):
        if (scp_doc.data["coredata"]['dc:description'] != ""):
            title = scp_doc.title
            print ("scp_doc.title: ", title)
            words = scp_doc.data['coredata']['dc:description']
            #wordabs = re.split(r'(?<=\w\.)\s', words)
            wordabs = words.replace(". ", ".\n")
            WriteToFile(title, wordabs)
            #scp_doc.write()   
        else:
            print("  Abstract not available")
    else:
        print ("Read document failed.")
        