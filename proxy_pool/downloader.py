import traceback
import requests
import chardet


class Downloader(object):
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }

    def download(self, url):
        try:
            resp = requests.get(url, headers=self.header)
            resp.encoding = chardet.detect(resp.content).get('encoding')

            if resp.status_code == 200:
                return resp.text

            else:
                raise ConnectionError

        except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    # d = Downloader()
    # print(d.header)
    pass
