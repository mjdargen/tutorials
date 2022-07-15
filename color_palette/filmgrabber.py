# Simple Script to get images from https://film-grab.com
# Stolen from here: https://github.com/v-za/film-grabber
import os
import errno
import argparse
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


base_url = "http://www.film-grab.com/"


def valid_url(url):
    # checks that URL is valid
    parsed_url = urlparse(url)
    return bool(parsed_url.netloc) and bool(parsed_url.scheme)


def get_images(film):
    film = film.lower().replace(" ", "-")
    url = base_url + film + "/"

    urls = []
    if valid_url(url):
        soup = bs(requests.get(url).content, "html.parser")
        for img in tqdm(soup.find_all("img"), "Collecting image URLs"):
            img_url = img.attrs.get("src").replace("/thumb", "")
            img_url = urljoin(url, img_url)
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass

            if valid_url(img_url):
                urls.append(img_url)

    else:
        print("Film not available")

    return urls


# Downloads a file given an URL and puts it in the folder `pathname`
def download(url, pathname):
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1].lower())
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(
        1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


def main():
    parser = argparse.ArgumentParser(
        description='Downloads still images from https://film-grab.com.')
    parser.add_argument("-f", "--film",
                        help='Name of film to search for.',
                        type=str, required=True)
    parser.add_argument("-p", "--path",
                        help='Output path to store images.',
                        type=str, default=".")
    args = parser.parse_args()

    cwd = os.path.dirname(os.path.realpath(__file__))
    path = os.path.normpath(os.path.join(cwd, args.path))
    if not os.path.exists(path):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path)

    imgs = get_images(args.film)
    for img in imgs:
        download(img, path)


if __name__ == '__main__':
    main()
