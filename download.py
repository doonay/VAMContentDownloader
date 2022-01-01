import requests
import os
#from logic import session, headers, cookies
import re


# Метод создает\игнорирует\добавляет отсутствующие директории.
# На вход принимает название категории,
# проверяет сначала базовую директорию, потом передаваемую на наличие
def mk_dirs(directory: str):
    if not os.path.exists('content'):
        os.mkdir('content')
        print('Директория content создана')

    if os.path.exists(directory):
        pass
    else:
        os.mkdir(directory)
        print('Директория', directory, 'создана')

def mk_shortcut(shortcut: str):
    pass
#'type of content': 'Guides',
# 'img link': 'https://1387905758.rsc.cdn77.org/data/avatars/s/13/13301.jpg',
# 'url of content': 'https://hub.virtamate.com/resources/genesis8character-wo-vam-de-tukautame-no-nihongo-guide-normal-ver-2.8692',
# 'download link': 'https://hub.virtamate.com/resources/genesis8character-wo-vam-de-tukautame-no-nihongo-guide-normal-ver-2.8692/download',
# 'name': 'Genesis8Character wo VaM de tukautame no nihongo guide (normal ver.) 2'
# описание}
def download(card: dict, session, headers, cookies):
    directory = 'content/' + card.get('type of content')
    mk_dirs(directory)

    r = session.get(card.get('img link'), headers=headers, cookies=cookies)

    name = re.sub(r'[\\/*?:"<>|]', '', card.get('name')) #читстим будущее имя файла от запрещенных символов
    with open(directory + '/' + name + '.jpg', "wb") as code:
        code.write(r.content)

    r = session.get(card.get('url of content'), headers=headers, cookies=cookies)

    with open(directory + '/' + name + '.var', "wb") as code:
        code.write(r.content)


#!!!устарел
def download_old(img_url: str, content_url: str, filename: str, content_type: str, session, headers, cookies):
    directory = 'content/' + content_type
    mk_dirs(directory)

    r = session.get(img_url, headers=headers, cookies=cookies)

    with open(directory + '/' + filename + '.jpg', "wb") as code:
        code.write(r.content)

    r = session.get(content_url, headers=headers, cookies=cookies)

    with open(directory + '/' + filename + '.var', "wb") as code:
        code.write(r.content)


if __name__ == '__main__':
    #{'type of content': 'Guides', 'img link': 'https://1387905758.rsc.cdn77.org/data/avatars/s/13/13301.jpg', 'url of content': 'https://hub.virtamate.com/resources/genesis8character-wo-vam-de-tukautame-no-nihongo-guide-normal-ver-2.8692', 'download link': 'https://hub.virtamate.com/resources/genesis8character-wo-vam-de-tukautame-no-nihongo-guide-normal-ver-2.8692/download', 'name': 'Genesis8Character wo VaM de tukautame no nihongo guide (normal ver.) 2'}
    #download({'type of content': 'Guides', 'img link': 'https://1387905758.rsc.cdn77.org/data/avatars/s/13/13301.jpg', 'url of content': 'https://hub.virtamate.com/resources/genesis8character-wo-vam-de-tukautame-no-nihongo-guide-normal-ver-2.8692', 'download link': 'https://hub.virtamate.com/resources/genesis8character-wo-vam-de-tukautame-no-nihongo-guide-normal-ver-2.8692/download', 'name': 'Genesis8Character wo VaM de tukautame no nihongo guide (normal ver.) 2'})
    test_card = {'type of content': 'Assets', 'img link': 'https://1387905758.rsc.cdn77.org/data/resource_icons/8/8793.jpg', 'url of content': 'https://hub.virtamate.com/resources/campfire.8793', 'download link': 'https://hub.virtamate.com/resources/campfire.8793/download', 'name': 'Campfire', 'about:': 'Fireplace'}
    download(test_card)