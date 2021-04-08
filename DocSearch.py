# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 17:42:09 2018

@author: s213984
"""

from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
import json, re

def WriteToFile(title, content, location):
    """ title = abstract file name, content = metadata + abstract, location = local directory to store downloads """
    with open(location + title.replace(':','-') + ".txt", 'w+') as file:
        file.write(content)
            
def CleanUp(str_input):
    str_cleaned = str_input.replace(". ", ".\n")
    return str_cleaned

class DocSearch:
    def __init__(self, key_filename):
        ## Load configuration
        con_file = open(key_filename)
        config = json.load(con_file)
        con_file.close()
        
        ## Initialize client
        self.client = ElsClient(config['apikey'])
        
        
    def NumDocs(self, search_entry, unlimited):
        """ self = class instance object, search_entry = user entered search, unlimited = True (for all results) or False (For first page results only)"""
        ## Initialize doc search object and execute search, retrieving all results
        self.doc_srch = ElsSearch(search_entry,'scidir')
        # Change get_all = True below to get all results. Beware, might return large count!!!
        #start_time = time.time()
        self.doc_srch.execute(self.client, get_all = unlimited) 
        #print("%s seconds" % (time.time() - start_time))
        print("Search has returned ", len(self.doc_srch.results), "results.")
        
    
    def GetFullDocs(self, metadata, directory):
        """ self = class instance object, metadata = (True/False) to add metadata to each file download, directory = local directory to store abstract downloads """
        self.client.local_dir = directory;
        
        # Set up regular expressions for start of abstract and references, and full-stops.
        abspatt = re.compile(r'Abstract')
        refpatt = re.compile(r'References')
        locstart = 0
        locend = 0
        
        ## Loop through results of document search
        for srch_result in self.doc_srch.results:    
            doc_uri = FullDoc(uri = srch_result['prism:url'])
            if doc_uri.read(self.client):
                return_data = doc_uri.data
                if (return_data['coredata']['openArchiveArticle'] != False):
                    return_title = doc_uri.title
                    #return_data = doi_doc.data
                    print ("Downloading: ", doc_uri.title)       
                    
                    # Find matches to abstract, references and full-stop
                    absmatch_start = abspatt.finditer(return_data['originalText'])
                    for match in absmatch_start:
                        locstart = match.start()
                        break
                    
                    refmatch_start = refpatt.finditer(return_data['originalText'])
                    for match in refmatch_start:
                        locend = match.start()
            
                    fulltext = return_data['originalText'][locstart:locend-1]
                    
                    fulltext_clean =  CleanUp(fulltext)
                    WriteToFile(return_title, fulltext_clean, directory)
                    print("Download Complete!")
                    
                else:
                    print("  Not an open source article.")
                
            else:
                print ("Read document failed.")
            