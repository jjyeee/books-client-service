'''
Author: shihan
Date: 2024-01-31 23:42:24
version: 1.0
description: 
'''
"""
Author: shihan
Date: 2024-01-31 10:28:56
version: 1.0
description: app
"""

from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/queryfromserver", methods=["GET"])
def query_from_server():
    url = os.environ.get("BOOKS_API_URL", "http://books-server1929.bkdmd8hjcvhwhtbh.uksouth.azurecontainer.io/books")
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()  # list
        id = request.args.get("id", "")
        title = request.args.get("title", "")
        author = request.args.get("author", "")
        publication_year = request.args.get("publication_year", "")
        genre = request.args.get("genre", "")
        if(id=="" and title=="" and author=="" and publication_year=="" and genre==""):
            return render_template("page2.html", data=repos)
        new_list = find_book(repos, id, title, author, publication_year, genre)
        return render_template("page2.html", data=new_list)
    else:
        return "fail to get response"
    

@app.route("/searchfromserver", methods=["POST"])
def searchfromserver():
    id = request.form.get("id")
    title = request.form.get("title")
    author = request.form.get("author")
    publication_year = request.form.get("pub")
    genre = request.form.get("genre")

    url = os.environ.get("BOOKS_API_URL", "http://books-server1929.bkdmd8hjcvhwhtbh.uksouth.azurecontainer.io/books")
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()  # list
        if(id=="" and title=="" and author=="" and publication_year=="" and genre==""):
            return render_template("page2.html", data=repos)
        new_list = find_book(repos, id, title, author, publication_year, genre)
        return render_template("page2.html", data=new_list)
    else:
        return "fail to get response"
    
def find_book(repos, id, title, author, publication_year, genre):
    ret = []
    for book in repos:
        if (
            (id != "" and book["id"] == int(id))
            or (title != "" and book["title"] == title)
            or (author != "" and book["author"] == author)
            or (
                publication_year != ""
                and book["publication_year"] == int(publication_year)
            )
            or (genre != "" and book["genre"] == genre)
        ):
            ret.append(book)

    # reduce redundancy
    seen_ids = set()
    new_list = []
    for d in ret:
        if d["id"] not in seen_ids:
            new_list.append(d)
            seen_ids.add(d["id"])
    return new_list

if __name__ == '__main__':
    app.run(debug=True)