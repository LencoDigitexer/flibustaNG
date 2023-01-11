import requests
from bs4 import BeautifulSoup
from lxml import html

domain = "http://flibusta.is"
reader = "https://omnireader.ru/#/reader?url="


def get_book_details(book_id):
    """Подробная информация о книге"""

    # создаём реквест на основе id книги
    page = requests.get(domain + "/b/" + str(book_id))
    # подготавливаем страницу для xpath парсинга
    tree = html.fromstring(page.content)

    # описание книги
    info = tree.xpath('/html/body/div/div[2]/div[1]/div/p/text()')
    if info:
        info = info[0]
    else:
        info = ""

    # сколько скачали и сколько страниц
    pages = tree.xpath('//*[@id="main"]/div[3]/span/text()')
    if pages:
        pages = pages[0]
    else:
        pages = ""

    # обложка книги
    image = tree.xpath('//*[@id="main"]/img/@src')
    if image:
        image = image[0]
    else:
        image = ""

    # авторы книги
    authors_list = []
    authors_fio = tree.xpath('/html/body/div/div[2]/div[1]/div/a')
    for author in authors_fio:
        # учитываем только ссылки с авторами (убираем ссылки "следить")
        if "/a/" in author.attrib["href"]:
            authors_list.append({
                "fio": author.text,
                "href": author.attrib["href"]
            })

    read = reader + domain + "/b/" + str(book_id) + "/download"

    # парсинг файлов для скачивания
    files_list = []
    urls = tree.xpath('/html/body/div/div[2]/div[1]/div/div[3]/a')
    for url in urls:
        if "/b/" in url.attrib["href"] and url.text != "(читать)":
            files_list.append({
                "file_name": url.text,
                "href": url.attrib["href"]
            })

    details = {
        "info": info,
        "pages": pages,
        "image": image,
        "authors": authors_list,
        "read": read,
        "files": files_list,
    }
    return details


def search(name):
    """поиск книги по названию и вызов функции парсинга книги"""

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

        res[i]["book"] = {
            "name": book_a_text,
            "details": get_book_details(book_a_href[3:])
        }

        i = i + 1

    return res
