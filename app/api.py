import requests
from bs4 import BeautifulSoup
from lxml import html

domain = "http://flibusta.is"
reader = "https://omnireader.ru/#/reader?url="


def get_book_details(book_id):

    result = requests.get(domain + "/b/" + str(book_id))

    data = BeautifulSoup(result.text, "lxml")

    info = data.select("#main > p")

    for root in info:
        info = root.get_text()

    image = data.select("#main > img")

    for root in image:
        image = domain + root["src"]

    download = reader + domain + "/b/" + str(book_id) + "/download"
    fb2 = domain + "/b/" + str(book_id) + "/fb2"
    epub = domain + "/b/" + str(book_id) + "/epub"
    mobi = domain + "/b/" + str(book_id) + "/mobi"
    pdf = domain + "/b/" + str(book_id) + "/pdf"

    details = {
        "info": info,
        "image": image,
        "download": download,
        "file": {
            "fb2": fb2,
            "epub": epub,
            "mobi": mobi,
            "pdf": pdf,
        },
    }
    return details


def search(name):

    result = requests.get(domain + "/booksearch?ask={}&chb=on".format(name))

    data = BeautifulSoup(result.text, "lxml")

    res = []
    i = 0
    els = data.select("#main > ul > li")
    for div in els:
        root = div.find_all("a")

        res.append({"book": {}})

        book_a_text = root[0].get_text()
        book_a_href = root[0].get("href")
        test = get_book_details(book_a_href[3:])

        res[i]["book"] = {"name": book_a_text, "details": test}

        for j in range(1, len(root)):

            author_a_text = root[j].get_text()
            authors_a_href = root[j].get("href")

            # print(author_a_text)
            # print(authors_a_href)

            # res[i]["authors"].append({"href": authors_a_href, "name": author_a_text})
        i = i + 1

    posts = [
        {
            "book": {
                "name": "Хулиномика 4.0. Хулиганская экономика. Ещё толще. Ещё длиннее",
            },
        },
        {
            "book": {
                "name": "Хулиномика 4.0. Хулиганская экономика. Ещё толще. Ещё длиннее [издание 2021 г.]",
            },
            "details": {
                "info": "Идеальный учебник для тех, кто не любит учиться по скучным талмудам!",
                "image": "https://flibusta.is/i/90/606390/cover.jpg",
                "download": "https://flibusta.is/b/606390/download",
                "file": {
                    "fb2": "https://flibusta.is/b/606390/fb2",
                    "epub": "https://flibusta.is/b/606390/epub",
                    "mobi": "https://flibusta.is/b/606390/mobi",
                    "pdf": "https://flibusta.is/b/606390/pdf",
                },
            },
            "authors": [{"href": "/a/235828", "name": "Алексей Викторович Марков"}],
        },
    ]

    for post in posts:
        print("--------")
        print(post)

    print("############")

    for ress in res:
        print("--------")
        print(ress)

    print(type(posts))
    print(type(res))
    return res
