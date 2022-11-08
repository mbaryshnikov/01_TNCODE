import config as cfg
from funcions.util import db_exec
import pandas as pd



class Url:
    def __init__(self, user):
        self.orig = input('Input URL:')
        self.domain = self.orig[8:self.orig.index('/', 8)]
        db_exec(cfg.FILE_NAME, f"INSERT INTO Urls (Domain, Url_orig, User_ID) VALUES ('{self.domain}', '{self.orig}', '{user}');")

    @staticmethod
    def url_finder():
        url_short = int(input('Input short URL: ')[-5:])
        try:
            url_orig = db_exec(cfg.FILE_NAME, f"SELECT * FROM Urls WHERE Url_ID = {url_short};")[0][2]
            print('Original URL: ', url_orig)
        except:
            print('Invalid short URL!')

    @staticmethod
    def urls_print():
        urls_data = db_exec(cfg.FILE_NAME, f"SELECT Domain, URL_ID, User_Name FROM Urls JOIN Users on Users.User_ID = Urls.User_ID ORDER BY Urls.Domain;")
        urls_list = list(map(lambda x: [x[0], f'https://{x[0]}/{str(x[1]).rjust(5, "0")}', x[2]], urls_data))
        columns = ('Domain Name', 'Short URL', 'Creator')
        print('-' * 50)
        df = pd.DataFrame(urls_list, columns=columns)
        print (df)
        print('-' * 50)
