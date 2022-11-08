import config as cfg
from funcions.user import User
from funcions.url import Url


def greater(user):
    print('-'*35)
    print('     URL Shortener')
    print('-'*35)
    print(f'Hallo, {user.name}!')
    print(cfg.MENU_DISCR)


def main():
    user = User()
    greater(user)
    while True:
        user_choice = input('What to do? >> ')
        try:
            exec(cfg.command_list[user_choice])
            print(cfg.MENU_DISCR)
        except KeyError:
            print('Invalid command')


if __name__ == '__main__':
    main()