from flask import render_template, request, send_file
from flask import Response
from flask import stream_with_context
from flask import Flask, send_from_directory
import requests
from app import app

from app import api

domain = "http://flibusta.is"


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        title = "Результаты поиска"
        user = {"nickname": query}  # выдуманный пользователь
        posts = api.search(query)
        return render_template("newlist.html",
                               title=title,
                               user=user,
                               posts=posts)

    title = "FlibustaNG"
    return render_template("index.html", title=title)


def file_proxy(path):
    '''Simple stream file proxy with Flask and Requests'''
    req = requests.get(path, stream=True)
    return Response(stream_with_context(req.iter_content(chunk_size=1024)),
                    content_type=req.headers['content-type'])


@app.route('/<index>/<path:filename>', methods=['GET', 'POST'])
def download(filename, index):
    '''return book image'''
    path = domain + "/" + index + "/" + filename
    return file_proxy(path)


@app.route('/ads.txt')
def ads():
    path = 'ads.txt'
    return render_template("ads.txt")


@app.route("/list")
def list():
    title = "Результаты поиска"
    language = request.args.get("language")
    return render_template("newlist.html", title=title)


@app.route("/form", methods=["GET", "POST"])
def form_example():
    if request.method == "POST":
        language = request.form.get("language")
        framework = request.form.get("framework")
        return """
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>""".format(
            language, framework)
    return """
              <form method="POST">
                  <div><label>Language: <input type="text" name="language"></label></div>
                  <div><label>Framework: <input type="text" name="framework"></label></div>
                  <input type="submit" value="Submit">
              </form>"""
