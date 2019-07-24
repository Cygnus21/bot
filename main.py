import vk_api
import requests, bs4
import re
import logging
from vk_api.longpoll import VkLongPoll, VkEventType

token = 'a9e54cf93f3b9a9ef5e8ca7e88bf12e7d645cf23bd574a6cdbf42e9afbd2425574409742c877deee462e2'
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

longpool = VkLongPoll(vk_session)


def auth(self, nickname, password):
    self.nickname = nickname
    self.password = password
    url = 'https://www.livelib.ru/'
    payload = {
        'user[login]': nickname,
        'user[password]': password
    }
    session = requests.Session
    session = requests.post(url, data=payload)
    print(session.content)
    session.cookies


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
                    message='Твой ник - %s' % nickname + '. Выбери что ты хочешь получить: случайную книгу из хотелок или узнать последнюю прочитанную книгу?',
                    random_id='111112',
                    keyboard=open("keyboard.json", "r", encoding="UTF-8").read()
                )

            if event.text == 'Последняя прочитанная книга':
                url_read = 'https://www.livelib.ru/reader/%s/read' %(nickname)
                print(url_read)
                r = requests.get(url_read)
                b = bs4.BeautifulSoup(r.text, 'lxml')
                book = b.select('brow-data brow-book-name')[0].get('title')
                print(book)
                vk.messages.send(
                    user_id=event.user_id,
                    message='Твоей последней прочитанной книгой была следующая книга:%s' % book,
                    random_id='121412'
                )

            if event.text == 'Cлучайная книга':
                vk.messages.send(
                    user_id=event.user_id,
                    message='Напиши свой пароль для входа на страницу в следующем виде: Пароль - 123456',
                    random_id='111112'
                )
            if re.match(r'Пароль', event.text):
                password_parse = re.split(r'-', event.text)
                print(password_parse)
                password = password_parse[1]
                print(password)
                auth(nickname, password)



