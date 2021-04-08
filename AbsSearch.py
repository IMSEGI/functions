# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 14:58:45 2018

@author: s213984 Alozie O.
"""
import json#, time
from elsapy.elsclient import ElsClient
from elsapy.elsdoc import AbsDoc
from elsapy.elssearch import ElsSearch
from scopus import ScopusSearch

def WriteToFile(title, content, location):
    """ title = abstract file name, content = metadata + abstract, location = local directory to store downloads """
    with open(location + title.replace(':','-') + ".txt", 'w+') as file:
        file.write(content)
            
def CleanUp(str_input):
    str_cleaned = str_input.replace(". ", ".\n")
    return str_cleaned
    
    
class AbsSearch:
    """ Creates an object which searches and downloads journal abstracts & metadata from scopus for a given user entry"""
    def __init__(self, key_filename):
        ## Load configuration
        con_file = open(key_filename)
        config = json.load(con_file)
        con_file.close()
        
        ## Initialize client
        self.client = ElsClient(config['apikey'])
        
    
    def NumAbstract(self, search_entry, unlimited):
        """ self = class instance object, search_entry = user entered search, unlimited = True (for all results) or False (For first page results only)"""
        ## Initialize doc search object and execute search, retrieving all results
        self.srch_result = ElsSearch(search_entry,'scopus')
        # Change get_all = True below to get all results. Beware, might return large count!!!
        #start_time = time.time()
        self.srch_result.execute(self.client, get_all = unlimited) 
        #print("%s seconds" % (time.time() - start_time))
        print("Search has returned ", len(self.srch_result.results), "results.")
        
    def NumAbstract_fast(self, search_entry, refresh):
        self.srch_fast = ScopusSearch(search_entry, refresh)
        print("Search has returned ", len(self.srch_fast.EIDS), "results.")
        
            
    def GetAbstract(self, metadata, directory):
        """ self = class instance object, metadata = (True/False) to add metadata to each file download, directory = local directory to store abstract downloads """
        self.client.local_dir = directory;
        ## Loop through results of document search
        for srch_result in self.srch_result.results:    
            scp_doc = AbsDoc(uri = srch_result['prism:url'])
            
            if scp_doc.read(self.client):
                abs_title = scp_doc.title
                meta_words = ""
                
                if (metadata):
                    meta_words = scp_doc.data['author'] + "\n" + scp_doc.data['affil'] + "\n" + scp_doc.data['year'] + "\n"               
                
                print ("Downloading: ", abs_title)
                abs_words = scp_doc.data['coredata']['dc:description']
                #wordabs = re.split(r'(?<=\w\.)\s', words)
                abs_words_clean = CleanUp(meta_words + abs_words)
                WriteToFile(abs_title, abs_words_clean, directory)
                print ("Download Complete!")   
            
            else:
                print ("Read document failed.")
                
    
        