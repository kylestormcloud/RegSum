'''
Kyle Cloud
RegSum Flask Application
Last update: February 25, 2020
'''

# Import the required tools from flask
from flask import Flask, render_template, request

# Import the Volume class
from functions import Volume

app = Flask(__name__)

# Instantiate the Document object for Title 13, Volume 1
# The same process could be applied to other volumes.
# The choice of a single volume simplifies the demostration. 
CFR = Volume('CFR_Title13_Volume1.xml')

# Get a list of the section numbers from the Volume object.
numbers = []
for section in CFR.sections:
    numbers.append(section.number)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", numbers=numbers)

@app.route("/summary", methods=["POST"])
def summary():
    
    # Retrieve the section number input by the user
    # from the home page.
    number = int(request.form["sectno"])
    print(number)

    # The search_by_number method returns a tuple.
    result = CFR.search_by_number(number)

    # The first element in the tuple "result" is True,
    # confirming that a section was found.
    
    # The second element is the Section object
    # whose number matches the user's input.
    
    # To get the Section object, assign "section" to
    # the second element of "result" (index 1).
    section = result[1]
    
    # The summary page will display both the summary
    # and the original text.
    text = section.text
    summary = section.summary
    
    return render_template("summary.html", number=str(number), text=text, summary=summary)

app.run(debug=False)
