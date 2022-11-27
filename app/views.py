from flask import render_template, request
from app import app

from app import api


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        title = "Результаты поиска"
        user = {"nickname": query}  # выдуманный пользователь
        posts = api.search(query)
        return render_template("list.html", title=title, user=user, posts=posts)

    title = "FlibustaNG"
    return render_template("index.html", title=title)


@app.route("/list")
def list():
    title = "Результаты поиска"
    language = request.args.get("language")
    return render_template("list.html", title=title)


@app.route("/form", methods=["GET", "POST"])
def form_example():
    if request.method == "POST":
        language = request.form.get("language")
        framework = request.form.get("framework")
        return """
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>""".format(
            language, framework
        )
    return """
              <form method="POST">
                  <div><label>Language: <input type="text" name="language"></label></div>
                  <div><label>Framework: <input type="text" name="framework"></label></div>
                  <input type="submit" value="Submit">
              </form>"""
