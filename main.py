from logic import Logic
import download
'''
Методы
#get_soup(link):
#на вход получаем ссылку (str), возвращаем его soup

#get_pagination_number(soup):
#получаем число кусков (страниц) бесконечной страницы

#get_categories_dict(soup):
#на вход получаем soup возвращаем категории (dict)

#get_pagination_list(link :str):
#на вход получаем ссылку на категорию (строка), возвращаем список кусков (страниц) с контентом согласно пагинации

#get_cards(piece_of_cake):
#дербаним отрезок на карточки, возвращаем массив

#get_download_link(url_of_content):
#служебный метод. типа паука. для выдергивания ссылки на скачивание. но практика показывает, что достаточно добавить к основной ссылке \download\
'''
logic = Logic()
soup = logic.get_soup(logic.url)
categories = logic.get_categories(soup)
categories_dict = logic.get_categories_dict(soup)
for category in categories:
    pagination_links = logic.get_pagination_links(categories_dict.get(category))
    pieces_of_cake = pagination_links

    for page in pagination_links:
        card = (logic.get_cards(page))
        print('Start downloading', card.get['name'])
        download.download(card, logic.session, logic.headers, logic.cookies)
