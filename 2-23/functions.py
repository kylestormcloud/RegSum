# -*- coding: utf-8 -*-
"""
Kyle Cloud
February 22, 2020

Clean XML Files

The purpose is to remove the <E> elements
from inside the <P> elements of the XML file
"""

# Import regular expressions
import re

# Import the sentence tokenizer from the natural language toolkit
from nltk.tokenize import sent_tokenize

# Import the summarize and keywords functions from gensim
from gensim.summarization import summarize, keywords

# Import ElementTree
import xml.etree.ElementTree as ET

# Define the function
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
    ratio = 2 / sent_count

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
        
        Not case-sensitive.
        '''
        
        return keyword.lower() == self.keyword
        
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
    '''

    def __init__(self, filename):
        
        tree = ET.parse(filename)
        root = tree.getroot()

        CFR_iter = root.iter()
        doc_dict = {}

        for element in CFR_iter:
            if element.tag == 'SECTION':
                section = element.find('SECTNO').text
                number = re.sub(r'[^0-9\-\.]', '', section) # Process that number
                number = re.sub(r'\..*$', '', number)
                number = int(number)
                if number not in doc_dict.keys(): # new section = new key
                    doc_dict[number] = []
                for child in element.getchildren():
                    if child.tag == 'P': # get all the paragraphs
                        text = re.sub(r'^\(.*[0-9].*\)', '', child.text)
                        doc_dict[number].append(text) # all them to the list
        
        sections = []
        
        for key in doc_dict.keys():
            number = key
            text = ' '.join(doc_dict[key])
            section = Section(number, text)
            sections.append(section)
        
        self.sections = sections
        
    def search_by_number(self, number):
        
        for section in self.sections:
            if section.number == number:
                return (True, section)
        
        return (False, None)
    
    def search_by_keyword(self, keyword):
        
        for section in self.sections:
            if section.keyword == keyword:
                return (True, section)
            
        return (False, None)
    
    
    

    
    
    
    
    
    
    
    
    
    
    