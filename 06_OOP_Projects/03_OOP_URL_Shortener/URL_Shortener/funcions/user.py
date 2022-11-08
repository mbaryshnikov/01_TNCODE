from funcions.util import db_exec
import getpass
import config as cfg

class User:
    def __init__(self):
        self.id = None
        wrong_counter = 0
        while self.id is None:
            login = input('Login: ')
            password = getpass.getpass('Password:')
            try:
                user_data = db_exec(cfg.FILE_NAME, f"SELECT * FROM Users WHERE User_Name='{login}' AND Password='{password}';") 
                self.id = user_data[0][0]
                self.name = user_data[0][1]
            except:
                print('Wrong login or/and password. Try again.')
                wrong_counter +=1
                if wrong_counter > 2:
                    exit()

    def __repr__(self) -> str:
        return f'{self.id} {self.name}'
        