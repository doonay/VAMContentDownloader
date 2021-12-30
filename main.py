#По разведданным, при нажатии на кнопку yes добавляется кук ('vamhubconsent': 'yes')
#https/hub.virtamate.com/resources/categories/scenes.3/

#https://hub.virtamate.com/resources/categories/scenes.3/?page=1&_xfRequestUri=/resources/categories/scenes.3/&_xfWithData=1&_xfToken=1640100032,8b806b61259061428c963fc00b1cf3e4&_xfResponseType=json
#...
#https://hub.virtamate.com/resources/categories/scenes.3/?page=55&_xfRequestUri=/resources/categories/scenes.3/&_xfWithData=1&_xfToken=1640100032,8b806b61259061428c963fc00b1cf3e4&_xfResponseType=json

#1. проходим проверку возраста

#2. разбираем меню <ol class="categoryList toggleTarget is-active"> и создаем соответствующие списки или словари, хз

#Scenes
#Looks
#Clothing
#Hairstyles
#Morphs
#Textures
#Plugins
#Assets
#Guides
#Other


from logic import Logic

logic = Logic()
print(logic.get_categories_dict(logic.get_soup(logic.url)))

#на вход получаем ссылку (str), возвращаем его soup
#get_soup(link):

#получаем число кусков (страниц) бесконечной страницы
#get_pagination_number(soup):

#на вход получаем soup возвращаем категории (dict)
#get_categories_dict(soup):

#на вход получаем ссылку на категорию (строка), возвращаем список кусков (страниц) с контентом согласно пагинации
#get_pagination_list(link :str):

#print(get_pagination_list('https://hub.virtamate.com/resources/categories/plugins.12/'))

#дербаним отрезок на карточки, возвращаем массив
#get_cards(piece_of_cake):

#print(get_cards('https://hub.virtamate.com/resources/categories/plugins.12/?page=1'))

#служебный метод. типа паука. для выдергивания ссылки на скачивание. но практика показывает, что достаточно добавить к основной ссылке \download\
#get_download_link(url_of_content):

#!!!устарело
#получаем категории (list) устарело
#get_categories(soup):

	

#!!!устарел
#получаем ссылки по пагинации (list) сразу на весь бесплатный контент, без отдельной категории (в дальнейшем возможно не понадобится)
#get_pagination_list_all(soup):

'''
['https://hub.virtamate.com/resources/categories/plugins.12/?page=1',
'https://hub.virtamate.com/resources/categories/plugins.12/?page=2', 
'https://hub.virtamate.com/resources/categories/plugins.12/?page=3', 
'https://hub.virtamate.com/resources/categories/plugins.12/?page=4', 
'https://hub.virtamate.com/resources/categories/plugins.12/?page=5', 
'https://hub.virtamate.com/resources/categories/plugins.12/?page=6', 
'https://hub.virtamate.com/resources/categories/plugins.12/?page=7', 
'https://hub.virtamate.com/resources/categories/plugins.12/?page=8', 
'https://hub.virtamate.com/resources/categories/plugins.12/?page=9']
'''


#перевести логическую часть в логику
#создать часть для работы с БД
#в основном файле оставить основную часть
