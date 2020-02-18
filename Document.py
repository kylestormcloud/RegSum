'''
Defines the Document class.
An object of the Document class has
a list of Page objects.

The constructor accepts a file name as an argument,
opens the file,
reads the file,
extracts the text from each page,
and creates the list of Page objects.
'''

###############################
import PyPDF2
from Page import Page
###############################

class Document():

    def __init__(self, filename):

        # Open the PDF file
        docfile = open(filename, 'rb')

        # Read the file object
        document = PyPDF2.PdfFileReader(docfile)

        # Make a list of Page objects
        pageList = []
        for pg in range(document.getNumPages()):
            pageList.append(Page(document, pg))
        self.pages = pageList

    def get_summary(self):

        # Prompt the user for a page number
        pg = int(input("Choose a page to summarize: "))

        # Print out the original text and the summary
        print("Original Text:\n" + self.pages[pg+1].text)
        print("\nSummary:\n" + self.pages[pg+1].summary)