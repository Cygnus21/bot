import requests
import bs4
import re
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = 'a9e54cf93f3b9a9ef5e8ca7e88bf12e7d645cf23bd574a6cdbf42e9afbd2425574409742c877deee462e2'
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

longpool = VkLongPoll(vk_session)


def auth(nickname, password): # пока нерабочая функция
    url = 'https://www.livelib.ru/'
    s = requests.Session()
    data = {'user[login]': nickname, 'user[password]': password}
    random_book = s.post(url=url, data=data)
    random_book = requests.get('https://www.livelib.ru/reader/%s/wish/random' % nickname)
    print(random_book.text)
    return random_book


while 1:
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.from_user: # Если написали в ЛС
                if event.text == 'Привет!':
                    username = requests.get('https://api.vk.com/method/users.get?user_ids=event.user_id&fields=bdate&access_token=token&v=5.95')
                    print(username.status_code)
                    print(username.content)
                    name = vk.users.get(
                        user_ids=event.user_id,
                        fields="first_name",
                        lang="ru"
                    )
                    print(name)
                    for word in name:
                        first_name = word.get('first_name')
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.user_id,
                        message='Привет, ' + str(first_name) + '. Напиши мне свой ник на livelib в следующем формате: "Мой ник - BookSwan"',
                        random_id="123456"
                    )

                if re.match(r'Мой ник', event.text):
                    nickname_parse = re.split(r'-', event.text)
                    print(nickname_parse)
                    nickname = nickname_parse[1]
                    print(nickname)
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Твой ник - %s' % nickname + '. Выбери что ты хочешь узнать: число твоих прочитанных книг или последнюю прочитанную книгу?',
                        random_id='111112',
                        keyboard=open("bot/keyboard.json", "r", encoding="UTF-8").read()
                    )

                if event.text == 'Последняя прочитанная книга':
                    url_read = 'https://www.livelib.ru/reader/%s/read' %(nickname)
                    print(url_read)
                    r = requests.get(url_read)
                    with open('bot/test.html', 'w') as test:
                        test.write(r.content.decode('utf-8'))
                    test = open('bot/test.html', 'r')
                    b = bs4.BeautifulSoup(test, 'html.parser')
                    book = b.select('a.brow-book-name.with-cycle')[0].get('title')
                    print(book)
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Твоей последней прочитанной книгой была следующая книга: %s' % book,
                        random_id='123312'
                    )

                if event.text == 'Случайная книга':  # пока не работает из-за авторизации
                    username = requests.get('https://api.vk.com/method/users.get?user_ids=event.user_id&fields=bdate&access_token=token&v=5.95')
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Напиши свой пароль для входа на страницу в следующем виде: Пароль - 123456',
                        random_id='143243'
                    )
                if re.match(r'Пароль', event.text):
                    password_parse = re.split(r'-', event.text)
                    print(password_parse)
                    password = password_parse[1]
                    print(password)
                    r = auth(nickname, password)
                    with open('bot/random.html', 'w') as test:
                        test.write(r.content.decode('utf-8'))
                    test = open('bot/random.html', 'r')
                    b = bs4.BeautifulSoup(test, 'html.parser')
                    book = b.select('a.brow-book-name.with-cycle').get('title')
                    print(book)
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Тебе выпала следующая книга: %s' % book,
                        random_id='121762'
                    )
                if event.text == 'Количество моих прочитанных книг':
                    url_read = 'https://www.livelib.ru/reader/%s' % (nickname)
                    print(url_read)
                    r = requests.get(url_read)
                    with open('bot/count.html', 'w') as test:
                        test.write(r.content.decode('utf-8'))
                    test = open('bot/count.html', 'r')
                    b = bs4.BeautifulSoup(test, 'html.parser')
                    book = b.select('a[href$="read"]')[0].contents[1].contents[0]
                    print(book)
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Общее количество прочитанных книг: %s' % book,
                        random_id='129521'
                    )



