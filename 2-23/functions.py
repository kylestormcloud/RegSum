# -*- coding: utf-8 -*-
"""
Kyle Cloud
Last Update: February 25, 2020

Notes:

This project uses the tools in Gensim, a Python library for topic modeling,
to summmarize sections of the Code of Federal Regulations.

Below I have attempted to give a concise overview of how summarization
with Gensim works. The points herein discussed come from Rare Technologies,
the creators of Gensim.
    
Gensim's summarization module:

from: https://rare-technologies.com/text-summarization-in-python-extractive-vs-abstractive-techniques-revisited/ 

   - unsupervised algorithm
   - based on weighted-graphs
   - built on PageRank
       - used by Google to rank webpages
   - uses Okapi BM25 function
   
TextRank:

from: https://rare-technologies.com/text-summarization-in-python-extractive-vs-abstractive-techniques-revisited/

    1. Pre-process the text:
        A. Remove stop words
        B. Stem remaining words
    2. Create a weighted graph
        - vertices are sentences
    3. All sentences connected to all others by edges
        - an edge's weight denotes the simialarity
          between the two sentences it connects
    4. Run PageRank algorithm
    5. Pick the sentences with the highest score.
      
PageRank:

from: https://en.wikipedia.org/wiki/PageRank
    
    - based on the webgraph
        - pages are nodes
        - hyperlinks are edges
    - counts number and quality of links to a page
    - outputs probability distribution random clicks will land you on a page
    
Okapi BM25:
 
from: https://en.wikipedia.org/wiki/Okapi_BM25
 
    - bag-of-words retrieval function
    - TF-IDF-like
    
Bag of Words:
    - Input = context
    - Predict: word
"""

# Import regular expressions
import re

# Import the sentence tokenizer from the natural language toolkit
from nltk.tokenize import sent_tokenize

# Import the summarize and keywords functions from gensim
from gensim.summarization import summarize, keywords

# Import ElementTree
import xml.etree.ElementTree as ET

# Preprocessing: removing unwanted elements from the original XML
def clean_xml(old_file, new_file):
    
    # Tell the user what's happening
    print("Creating %s from %s..." % (new_file,old_file))
    
    # Open the old file
    dirty_file = open(old_file)
    
    # Read the lines of the old file into a list
    dirty_list = dirty_file.readlines()
    
    # Create a new list
    clean_list = [] # Initialize the new list
    gpo = False
    for dirty_line in dirty_list: # Iterate through the old list
        clean_line = re.sub(r'<E .*?>', '', dirty_line) # remove the <E> elements
        clean_line = re.sub(r'</E>', '', clean_line)
        clean_line = re.sub(r'<PRTPAGE.*/>', '', clean_line) # remove PRTPAGE elements
        if '<GPOTABLE' in clean_line:
            gpo = True
        if gpo == False:
            clean_list.append(clean_line)
        if '/GPOTABLE' in clean_line:
            gpo = False
        
    # Create and open a new file
    clean_file = open(new_file, 'x')
    
    # Write the contents of the new list to the new file
    clean_file.writelines(clean_list)
    
    # Close the new file
    clean_file.close()
    
#####################################################################

# Preprocessing: clean up the text by removing indexing,
# citations, and newlines.
def preprocess(text):
    
    # Remove all indexing
    text = re.sub(r'\(\w{,5}\)', '', text)
    
    # Remove citations
    text = re.sub(r'\(.*[0-9].*\)', '', text)
    
    # Remove newlines
    text = re.sub(r'\n', ' ', text)
    
    return text

#####################################################################
   
def get_summary(text):

    # preprocess the text
    prepro = preprocess(text)
        
    # count the sentences
    sentences = sent_tokenize(prepro)
    sent_count = len(sentences)
        
    # compute the summary to text ratio
    ratio = 2 / sent_count # looking for one or two sentences per section

    # call the summarize function
    summary = summarize(prepro, ratio)
        
    return summary

#####################################################################
    
def get_keyword(text):
    
    # preprocess the text
    prepro = preprocess(text)
    
    # get a string of keywords
    kw_string = keywords(prepro)
    
    # split the string to form a list
    kw_list = kw_string.split('\n')
    
    # take the first element in the list
    keyword = kw_list[0]
    
    # make it lowercase
    keyword = keyword.lower()
    
    return keyword
    
#####################################################################

class Section():

    '''
    A Section object shall have four properties:
        - section number
        - original text
        - summary text
        - keyword
    '''
    
    
    def __init__(self, number, text):
        
        # number: simply the section number as indicated in the text
        self.number = number
        
        # text: the raw text of the section
        self.text = text
        
        # summary: a summary of the section text
        self.summary = get_summary(text)
        
        # keyword: the word that is most relevant to the sectiom
        self.keyword = get_keyword(text)
        
    def keyword_match(self, keyword):
        
        '''
        Check if a word input by the user
        matches the keyword of the section.
        
        Not case-sensitive since both the user
        input and keyword attribute are converted
        to lowercase for the comparison
        '''
        
        return keyword.lower() == self.keyword.lower()
        
    def number_match(self, number):
        
        '''
        Check if a number input by the user
        matchs the number of the section.
        '''
        
        return number == self.number

#####################################################################
        
class Volume():
    
    '''
    A Volume object contains a collection of Section objects.
    
    It offers functionality to search for a section by
    number or keyword.
    
    The constructor accepts the name of the XML file
    from which the Volume object will be created
    '''

    def __init__(self, filename):
        
        # Create an ElementTree for the XML file
        tree = ET.parse(filename)
        
        # Get the root node
        root = tree.getroot()

        # Create an iterator to iterate through the elements
        CFR_iter = root.iter()
        doc_dict = {} # dictionary to hold sections and respective text

        for element in CFR_iter:
            if element.tag == 'SECTION':
                section = element.find('SECTNO').text # Get the section number
                number = re.sub(r'[^0-9\-\.]', '', section) # Trim the number
                number = re.sub(r'\..*$', '', number) # Ignore subsection numbers
                number = int(number) # convert to integer
                if number not in doc_dict.keys(): # new section = new key
                    doc_dict[number] = [] # new section: start with an empty list
                for child in element.getchildren():
                    if child.tag == 'P': # get all the paragraphs
                        text = re.sub(r'^\(.*[0-9].*\)', '', child.text)
                        doc_dict[number].append(text) # append text to the list
        
        sections = [] # Initialize a list to hold the Section objects
        
        for key in doc_dict.keys(): # Iterate through the dictionary
            number = key # The keys are the numbers of each section
            text = ' '.join(doc_dict[key]) # The texts are the values, join lists into strings
            section = Section(number, text) # Instantiate an object for each section, and...
            sections.append(section) # append it to the Volume sections list
        
        self.sections = sections # That list becomes the attribute of the Volume object.
        
    def search_by_number(self, number):
        
        for section in self.sections:
            if section.number == number:
                return (True, section)
        
        return (False, None)
    
    def search_by_keyword(self, keyword):
        
        '''
        Accepts a keyword and returns a list of sections whose keyword matches the input.
        '''
        
        match_list = [] # Initialize the list of matches
        
        for section in self.sections: # Iterate through the sections.
            if section.keyword == keyword: # If there is a match,...
                match_list.append(section) # ...append that section to the list.
            
        return match_list
    
    
    

    
    
    
    
    
    
    
    
    
    
    
