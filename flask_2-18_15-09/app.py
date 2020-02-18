from flask import Flask, render_template, request
from Document import Document

app = Flask(__name__)

# Instantiate the Document object for Title 13
CFR = Document('CFR-2019-title13-vol1.pdf')

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/summary", methods=["POST"])
def summary():
    
    pageNum = int(request.form["page number"])
    
    page = CFR.pages[pageNum-1]
    
    text = page.text
    summary = page.summary
    
    return render_template("summary.html", text=text, summary=summary)

app.run(debug=True)