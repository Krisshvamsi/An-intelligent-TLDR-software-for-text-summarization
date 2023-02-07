from flask import Flask, render_template, request, url_for
from scraper import scraper
from summarizer import summarizer, estimated_reading_time

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route("/")
def home():
        return render_template("main.html")

@app.route("/text", methods=['GET', 'POST'])
def text():
    if request.method == 'POST':
        text = request.form.get('text')
        summary = summarizer(text)
        reading_time = estimated_reading_time(summary.split())
        return render_template("text.html",reading_time = reading_time, summary = summary)

    else: 
        return render_template("text.html")


@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')

        try:
            article_title, text = scraper(url)
            summary = summarizer(text)
            reading_time = estimated_reading_time(summary.split())
            return render_template("index.html", article_title = article_title, reading_time = reading_time, summary = summary)
        
        except TypeError():
            print('Invalid url entered')

    else: 
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)