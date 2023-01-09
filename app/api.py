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

    authors_list = []

    # авторы книги
    authors_fio = tree.xpath('/html/body/div/div[2]/div[1]/div/a')
    for author in authors_fio:
        # учитываем только ссылки с авторами (убираем ссылки "следить")
        if "/a/" in author.attrib["href"]:
            authors_list.append({
                "fio": author.text,
                "href": author.attrib["href"]
            })

    # парсинг файлов для скачивания
    files = {}
    read = reader + domain + "/b/" + str(book_id) + "/download"

    download_url = tree.xpath('//*[@id="main"]/div[3]/a/@href')
    download_text = tree.xpath('//*[@id="main"]/div[3]/a/text()')

    # если ссылка единственная и это не кнопка "читать"
    if (download_url and (download_text[0] != "(читать)")):
        files["download_url"] = download_url[0]
        files["download_text"] = download_text[0]
    else:

        url = tree.xpath('/html/body/div/div[2]/div[1]/div/div[3]/a[2]/@href')
        url_text = tree.xpath(
            '/html/body/div/div[2]/div[1]/div/div[3]/a[2]/text()')

        fb2 = tree.xpath('/html/body/div/div[2]/div[1]/div/div[3]/a[3]/@href')
        fb2_text = tree.xpath(
            '/html/body/div/div[2]/div[1]/div/div[3]/a[3]/text()')

        epub = tree.xpath('/html/body/div/div[2]/div[1]/div/div[3]/a[4]/@href')
        epub_text = tree.xpath(
            '/html/body/div/div[2]/div[1]/div/div[3]/a[4]/text()')

        mobi = tree.xpath('/html/body/div/div[2]/div[1]/div/div[3]/a[5]/@href')
        mobi_text = tree.xpath(
            '/html/body/div/div[2]/div[1]/div/div[3]/a[5]/text()')

        pdf = tree.xpath('/html/body/div/div[2]/div[1]/div/div[3]/a[6]/@href')
        pdf_text = tree.xpath(
            '/html/body/div/div[2]/div[1]/div/div[3]/a[6]/text()')

        if url and url_text[0] != "(читать)":
            files["url"] = url[0]
            files["url_text"] = url_text[0]

        if fb2:
            files["fb2"] = fb2[0]
            files["fb2_text"] = fb2_text[0]

        if epub:
            files["epub"] = epub[0]
            files["epub_text"] = epub_text[0]

        if mobi:
            files["mobi"] = mobi[0]
            files["mobi_text"] = mobi_text[0]

        if pdf:
            files["pdf"] = pdf[0]
            files["pdf_text"] = pdf_text[0]

    details = {
        "info": info,
        "pages": pages,
        "image": image,
        "authors": authors_list,
        "read": read,
        "file": files,
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
