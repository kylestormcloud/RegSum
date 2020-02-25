from flask import Flask, render_template, request
from functions import Volume

app = Flask(__name__)

# Instantiate the Document object for Title 13
CFR = Volume('CFR_Title13_Volume1.xml')

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/summary", methods=["POST"])
def summary():
    
    number = int(request.form["sectno"])
    print(number)

    result = CFR.search_by_number(number)

    section = result[1]
    
    text = section.text
    summary = section.summary
    
    return render_template("summary.html", number=str(number), text=text, summary=summary)

app.run(debug=False)
