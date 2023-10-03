import os
import shutil
import urllib
import posixpath
import requests
from tqdm import tqdm
from urllib import request
from urllib.parse import quote


class ImageDownloader:
    def __init__(self,
                 query: str = '',
                 limit: int = 10,
                 output_dir: str = 'temp_folder',
                 overwrite_old_folder: bool | int = False,
                 timeout: int = 5,
                 verbose: bool | int = False):
        self.query = query
        self.limit = limit
        self.output_dir = f'{output_dir}/IMDB/{self.query.replace(" ", "_")[:15]}'
        # ----------------------------------------------------------------------------
        self.overwrite_old_folder = overwrite_old_folder if overwrite_old_folder in [0, 1, False, True] else True
        if os.path.isdir(self.output_dir):
            if self.overwrite_old_folder:
                try:
                    shutil.rmtree(self.output_dir, ignore_errors=True)
                    os.makedirs(self.output_dir, exist_ok=True)
                except PermissionError as perm:
                    print(perm)
        else:
            self.overwrite_old_folder = 1
            os.makedirs(self.output_dir, exist_ok=True)
        # ----------------------------------------------------------------------------
        self.timeout = timeout
        self.verbose = verbose if verbose in [0, 1, False, True] else False
        self.download_count = 0
        self.extensions = ['jpg', 'jpeg', 'jpe', 'jif', 'jfif', 'jfi', 'jp2', 'jps',
                           'png', 'gif', 'webp', 'tiff', 'tif']
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/116.0.0.0 "
                                      "Safari/537.36"}
        self.request_url = f"https://v2.sg.media-imdb.com/suggestion/" \
                           f"{self.query[0]}/{self.query.replace(' ', '_')}.json"

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
        res = requests.get(self.request_url)
        res_dict = res.json()
        links = list()
        if 'd' in res_dict:
            for line in res_dict['d']:
                if 'i' in line:
                    if 'imageUrl' in line['i']:
                        links.append(line['i']['imageUrl'])
        if self.verbose:
            print(f"\n==============================================="
                  f"\n[%] Indexed {len(links)} Images."
                  f"\n===============================================\n")
            pbar = None
        else:
            pbar = tqdm(total=min(len(links), self.limit), desc="Downloading: ", unit="image")
        for link in links:
            if not self.verbose:
                pbar.refresh()
            if self.download_count < self.limit:
                update_pbar = self.download_image(link)
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
            try:
                self.main_loop()
            except Exception as error:
                if self.verbose:
                    print(error)
        return self.output_dir


def downloader(query: str = '',
               limit: int = 20,
               output_directory: str = 'Image downloads',
               overwrite: bool | int = False,
               timeout: int = 5,
               verbose: bool | int = False):
    """This library downloads images from IMDB images by a search term (query)

    query - Search term, can be anything!
    limit - Number of images to download. (If there are fewer images than limit, stopping after downloading all of them)
    output_directory - Output directory for downloaded images.
    overwrite - Overwrite the output folder tree. (Will delete previous query search results)
    timeout - Timeout after requesting an image
    verbose - Print to the screen the full process. (Breaks the progress bar, so it won't be shown when enabled)
    """
    try:
        download = ImageDownloader(query, limit, output_directory, overwrite, timeout, verbose)
        return download.run()
    except Exception as error:
        if verbose:
            print(error)
