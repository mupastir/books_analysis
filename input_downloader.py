import requests
from zipfile import ZipFile
from subprocess import call


class InputDownloader:
    raw_zip_file = 'book_raw.zip'

    def __init__(self, file_url: str):
        self.file_url = file_url

    def run(self):
        self._download_input()
        self._extract_input()

    def _download_input(self):
        proxies = self._get_proxies()
        r = requests.get(self.file_url,
                         stream=True)
        with open(self.raw_zip_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

    def _extract_input(self):
        with ZipFile(self.raw_zip_file, 'r') as books_zip:
            books_zip.extractall('_input')

    def _get_proxies(self) -> dict:
        call('proxies.py', shell=True)
        proxy_dict = {}
        with open('proxies.txt', 'r') as pl:
            for p in pl.readlines():
                clean_proxy = p.strip()
                proxy_type, _ = clean_proxy.split(':')
                if proxy_type in proxy_dict:
                    proxy_dict[proxy_type].append(clean_proxy)
                else:
                    proxy_dict[proxy_type] = [clean_proxy]
        return proxy_dict
