import os
import re
import shutil
import urllib
import posixpath
from tqdm import tqdm
from urllib import request
from urllib.parse import quote


class ImageDownloader:
    # ----------------------------------------------------------------
    # reworked by Idan Achrak
    # modified for easier run and support for google images
    # Originally created by:
    # ----------------------------------------------------------------
    # Name: bing-image-downloader
    # Version: 1.0.4
    # Summary: Python library to download bulk images from Bing.com
    # Home-page: https://github.com/gurugaurav/bing_image_downloader
    # Author: Guru Prasad Singh
    # Author-email: g.gaurav541@gmail.com
    # ----------------------------------------------------------------
    # MIT License
    #
    # Copyright (c) 2020 Guru Prasad Singh
    #
    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:
    #
    # The above copyright notice and this permission notice shall be included in all
    # copies or substantial portions of the Software.
    #
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    # SOFTWARE.
    # ----------------------------------------------------------------
    # The following is a modified version of the package mentioned above:
    def __init__(self, search_engine: str = 'google',
                 query: str = '',
                 limit: int = 10,
                 output_dir: str = 'temp_folder',
                 overwrite_old_folder: bool | int = False,
                 adult_filter: bool | int = False,
                 timeout: int = 5,
                 verbose: bool | int = False):
        temp = search_engine.lower()
        self.search_engine = temp if temp in ['google', 'bing'] else 'google'
        self.query = query
        self.limit = limit
        self.output_dir = f'{output_dir}/{self.search_engine}/{self.query.replace(" ", "_")[:15]}'
        # ----------------------------------------------------------------------------
        self.overwrite_old_folder = overwrite_old_folder if overwrite_old_folder in [0, 1, False, True] else True
        if os.path.isdir(self.output_dir):
            if self.overwrite_old_folder:
                try:
                    shutil.rmtree(self.output_dir)
                    os.makedirs(self.output_dir, exist_ok=True)
                except PermissionError as perm:
                    print(perm)
        else:
            self.overwrite_old_folder = 1
            os.makedirs(self.output_dir, exist_ok=True)
        # ----------------------------------------------------------------------------
        self.adult = 'on' if adult_filter else 'off'
        self.timeout = timeout
        self.verbose = verbose if verbose in [0, 1, False, True] else False
        self.download_count = 0
        self.extensions = ['jpg', 'jpeg', 'jpe', 'jif', 'jfif', 'jfi', 'jp2', 'jps',
                           'png', 'gif', 'webp', 'tiff', 'tif']
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/116.0.0.0 "
                                      "Safari/537.36"}
        if self.search_engine == 'google':
            self.request_url = f'https://www.google.com/search?q={urllib.parse.quote_plus(self.query)}' \
                               f'&source=lnms' \
                               f'&tbm=isch' \
                               f'&safe={self.adult}'
            self.string = r'\["https(.*?)",'
            self.link_header = 'https'
        elif self.search_engine == 'bing':
            self.request_url = f'https://www.bing.com/images/search?q={urllib.parse.quote_plus(self.query)}' \
                               f'&adlt={self.adult}'
            self.string = 'murl&quot;:&quot;(.*?)&quot;'
            self.link_header = ''

    def save_image(self, link, file_path):
        request_image = urllib.request.Request(link, None, self.headers)
        image = urllib.request.urlopen(request_image, timeout=self.timeout).read()
        with open(file_path, 'wb') as f:
            f.write(image)

    def download_image(self, link):
        # Get the image link
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split('?')[0]
            file_type = filename.split(".")[-1]
            if file_type.lower() in self.extensions:
                # Download the image
                if self.verbose:
                    print(f"[%] Downloading from {link}")
                self.save_image(link, f'{self.output_dir}/{self.download_count + 1}.{file_type}')
                if self.verbose:
                    print(f"[%] Image #{self.download_count + 1} Downloaded !\n########################")
                self.download_count += 1
                return True
        except Exception as exc:
            if self.verbose:
                print(f"[!] Issue getting: {link}\n[!] Error:: {exc}\n########################")
        return False

    def main_loop(self):
        # Parse the page source and download pics
        temp_request = urllib.request.Request(self.request_url, None, headers=self.headers)
        temp_response = urllib.request.urlopen(temp_request)
        html = temp_response.read().decode('utf8')
        links = re.findall(self.string, html)
        if self.verbose:
            print(f"\n==============================================="
                  f"\n[%] Indexed {len(links)} Images."
                  f"\n===============================================\n")
            pbar = None
        else:
            pbar = tqdm(total=min(len(links), self.limit), desc="Downloading: ", unit=" images")
        for link in links:
            if not self.verbose:
                pbar.refresh()
            if self.download_count < self.limit:
                update_pbar = self.download_image(f'{self.link_header}{link}')
                if not self.verbose:
                    if update_pbar:
                        pbar.update()
            elif self.download_count == len(links):
                if self.verbose:
                    print(f"\n\n[%] Done. Downloaded all indexed images ({self.download_count} images).")
                    print("\n===============================================\n")
                break
            else:
                if self.verbose:
                    print(f"\n\n[%] Done. Downloaded {self.download_count} images.")
                    print("\n===============================================\n")
                break
        if self.download_count < self.limit and self.verbose:
            print(f"\n\n[%] Done. Downloaded all non-restricted images ({self.download_count} images).")
            print("\n===============================================\n")

    def run(self):
        if self.overwrite_old_folder and self.query.replace(' ', '') != '':
            self.main_loop()
        return self.output_dir


def downloader(search_engine: str = 'google',
               query: str = '', 
               limit: int = 20,
               output_directory: str = 'Image downloads',
               overwrite: bool | int = False,
               adult_filter: bool | int = False,
               timeout: int = 5,
               verbose: bool | int = False):
    """This library downloads images from Google/Bing images by a search term (query)

    search_engine - Compatible strings: 'google'/'bing' (Can work with caps - GoOgLe). Defaults to 'google'.
    query - Search term, can be anything!
    limit - Number of images to download. (If there are fewer images than limit, stopping after downloading all of them)
    output_directory - Output directory for downloaded images.
    overwrite - Overwrite the output folder tree. (Will delete previous query search results)
    adult_filter - Filter adult images from search.
    timeout - Timeout after requesting an image
    verbose - Print to the screen the full process. (Breaks the progress bar, so it won't be shown when enabled)
    """
    download = ImageDownloader(search_engine, query, limit, output_directory, overwrite, adult_filter, timeout, verbose)
    return download.run()
