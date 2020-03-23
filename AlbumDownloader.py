import os
import re
import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text


def get_all_albums_names(html):
    result = []
    soup = BeautifulSoup(html, 'lxml')
    albums = soup.find_all('h3', class_="h3 g-font-weight-500 mb-1")
    result = re.findall('<h3 class="h3 g-font-weight-500 mb-1">(.+?)</h3>', str(albums))
    for i in range(len(result)):
        result[i] = result[i].replace("\"", "")
    return result


def get_all_album_links(html):
    result = []
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('a', class_="u-link-v2")
    result = re.findall('<a class="u-link-v2" href="/media/photo/(.+?)"></a>', str(links))
    return result


def get_all_photo_names(html):
    result = []
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('img', class_="img-fluid u-block-hover__main--grayscale u-block-hover__img")
    result = re.findall('<img class="img-fluid u-block-hover__main--grayscale u-block-hover__img" src="/upload/iblock/.+?/(.+?)"/>', str(links))
    return result


def get_all_photo_links(html):
    result = []
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('img', class_="img-fluid u-block-hover__main--grayscale u-block-hover__img")
    result = re.findall('<img class="img-fluid u-block-hover__main--grayscale u-block-hover__img" src="(.+?)"/>', str(links))
    return result


def link_concatenate(url, link):
    result = [url] * len(link)
    for i in range(len(link)):
        result[i] += link[i]
    return result


def save_photo(album_name, album_link, url):
    photo_links = link_concatenate(url, get_all_photo_links(get_html(album_link)))
    photo_names = get_all_photo_names(get_html(album_link))
    print("Создание папки " + album_name)
    os.mkdir(album_name)
    print("Изменение директории на " + album_name)
    os.chdir(album_name)
    for i in range(len(photo_links)):
        img_data = requests.get(photo_links[i]).content
        with open(photo_names[i], 'wb') as handler:
            handler.write(img_data)
        print("Файл " + photo_names[i] + " загружен!")
    os.chdir('..')
    print("Возврат назад на одну папку.\n\n")


def main_photo(url):
    album_names = get_all_albums_names(get_html(url))
    album_links = link_concatenate(url, get_all_album_links(get_html(url)))
    new_url = re.findall('(.+?)/media/photo/', str(url))[0]
    os.mkdir("Photos")
    os.chdir("Photos")
    for i in range(len(album_links)):
        save_photo(album_names[i], album_links[i], new_url)


url = "https://student.mirea.ru/media/photo/"
main_photo(url)
