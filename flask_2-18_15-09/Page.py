'''
Defines the Page class.
An object of the Page class has
the text of a page,
the summary of the text,
and the keywords.
'''

#####################################################
from gensim.summarization import summarize, keywords
import re
#####################################################

class Page():

    def __init__(self, document, pageNum):
        
         # Take a page out of the document:
        page = document.getPage(pageNum)

        # Extract text
        text = page.extractText()

        # Preprocess text
        text = self.preprocess(text)
        
        self.text = text
        self.summary = self.summarize(0.05)
        self.keywords = keywords(text, ratio=0.02)

    # Add functionality for changing ratio
    def change_ratio(self, ratio):
        self.summary = self.summarize(ratio)

    # Capitalize the first letter in the sentence
    def summarize(self, ratio):
        try:
            summary = summarize(self.text, ratio=ratio)
        except ValueError:
            summary = self.text
        if len(summary) > 1:
            summary = summary[0].upper() + summary[1:]
        #summary = summary[0].upper() + summary[1:]
        return summary

    # Keyword check
    def match(self, word):
        return word in self.keywords

    def preprocess(self, text):

        # Remove the first line
        text = re.sub(r'^.+?\n','',text)

        # Remove metadata at the end of the page
        text = re.sub(r'VerDate.*$','',text)

        # Convert to all lowercase
        text = text.lower()

        # Join split words
        text = re.sub(r'\-\n','',text)

        # Remove headers
        text = re.sub(r'\(\w{1,4}\)','',text)

        # Remove § section headers
        text = re.sub(r'§[0-9]+\.[0-9]+','',text)

        # Remove numbers and special characters
        text = re.sub(r'[^ \.a-zA-Z]', '', text)

        # Change all whitespace to one space
        text = re.sub(r'\s+',' ',text)
    
        return text
