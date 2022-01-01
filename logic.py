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



import requests
from bs4 import BeautifulSoup as bs
from db import Database
import download
from time import sleep
import lxml

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}
cookies = {'vamhubconsent': 'yes'}

class Logic():
	def __init__(self, base_url='https://hub.virtamate.com', url='https://hub.virtamate.com/resources/categories/free.4/?page=1'):
		self.base_url = base_url
		self.url = url
		self.session = session
		self.headers = headers
		self.cookies = cookies

	# создаем запрос
	# на вход получаем ссылку (str), возвращаем его soup
	def get_soup(self, link):
		r = session.get(link, headers=headers, cookies=cookies) # подсунули свой кук с согласием
		soup = bs(r.content, 'lxml')
		return soup

	#получаем число кусков (страниц) бесконечной страницы
	def get_pagination_number(self, soup):
		x = int(soup.find('div', {'class': "menu menu--pageJump", 'data-menu': "menu", 'aria-hidden': "true"}).find('input', {'type': "number"}).get('max'))
		return x

	#на вход получаем soup возвращаем категории (dict)
	def get_categories_dict(self, soup):
		cards = soup.find('ol', class_="categoryList toggleTarget is-active").find('li', class_="categoryList-item").find('ol', class_="categoryList toggleTarget is-active")#.find('ol', class_="categoryList toggleTarget is-active"))#.find_all('li', class_="categoryList-item"))
		bards = cards.find_all('li', class_="categoryList-item")

		categories = {}
		for e in bards:
			#<a class="categoryList-link" href="/resources/categories/scenes.3/">
			key = e.find('div', class_="categoryList-itemRow").find('a').text.strip()
			value = self.base_url + e.find('div', class_="categoryList-itemRow").find('a').get('href')[0:-1]
			categories[key] = value
		return categories

	#print(get_categories_dict(get_soup(url)))

	#на вход получаем ссылку на категорию (строка), возвращаем список кусков (страниц) с контентом согласно пагинации
	def get_pagination_links(self, link):
		soup = self.get_soup(link)
		x = self.get_pagination_number(soup)
		pagination_list = []
		for i in range(x):
			url = link + '?page={}'.format(i+1)
			pagination_list.append(url)

		return pagination_list

	#print(get_pagination_list('https://hub.virtamate.com/resources/categories/plugins.12/'))

	#дербаним отрезок на карточки, возвращаем массив
	#<div class="structItem structItem--resource is-prefix2  js-inlineModContainer js-resourceListItem-13253" data-author="misterx">
	def get_cards(self, piece_of_cake):
		#piece_of_cake = 'https://hub.virtamate.com/resources/categories/scenes.3/?page=1'
		#r = self.session.get(piece_of_cake, headers=self.headers, cookies=self.cookies)
		#soup = bs(r.content, 'lxml')
		soup = self.get_soup(piece_of_cake)
		#print(soup)
		cards = soup.find_all('div', class_="structItem")
		final_card = {}
		for card in cards:
			try:
				#type of content
				final_card['type of content'] = card.find('span', {'class': "label label--silver", 'dir': "auto"}).text
			except AttributeError:
				final_card['type of content'] = 'Other'

			# img link
			img_link = card.find('img').get('src')
			if img_link.find('https://') == 0:
				x = img_link.rfind('?')
				final_card['img link'] = img_link[:x]
			else:
				final_card['img link'] = 'https://hub.virtamate.com/logos/vam_logo_hub_trans_400x80.png'

			#url of content
			url_of_content = self.base_url + card.find('a', {'class': ""}).get('href')
			final_card['url of content'] = url_of_content[0:-1]

			#download link
			#print('download link:', base_url + get_download_link(url_of_content))
			final_card['download link'] = url_of_content + 'download'

			#name
			final_card['name'] = card.find('a', {'class': ""}).text

			#about
			final_card['about:'] = card.find('div', class_="structItem-resourceTagLine").text

		return final_card
	#print(get_cards('https://hub.virtamate.com/resources/categories/plugins.12/?page=1'))



	#служебный метод. типа паука. для выдергивания ссылки на скачивание. но практика показывает, что достаточно добавить к основной ссылке /download
	def get_download_link(self, url_of_content):
		#<a href="/resources/version-ii-four-pose-anal.13228/download" class="button--cta button button--icon button--icon--download" data-xf-click="overlay"><span class="button-text">Download</span></a>
		#url_of_content = 'https://hub.virtamate.com/resources/calister-secor-lookalike.13212/'
		#r = self.session.get(url_of_content, headers=self.headers, cookies=self.cookies)
		#soup = bs(r.content, 'lxml')
		#soup = self.get_soup(url_of_content)
		#print(soup)
		download_link = url_of_content + '/download'
		return download_link


	#!!!устарело
	#получаем категории (list) устарело
	def get_categories(self, soup):
		cards = soup.find('ol', class_="categoryList toggleTarget is-active").find('li', class_="categoryList-item")#.find('ol', class_="categoryList toggleTarget is-active"))#.find_all('li', class_="categoryList-item"))
		bards = cards.find('ol', class_="categoryList toggleTarget is-active").find_all('li', class_="categoryList-item")
		categories = []
		for e in bards:
			categories.append(e.find('div', class_="categoryList-itemRow").find('a').text.strip())
		return categories



	'''
	'https://hub.virtamate.com/resources/categories/plugins.12/?page=1',
	'https://hub.virtamate.com/resources/categories/plugins.12/?page=2', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=3', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=4', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=5', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=6', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=7', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=8', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=9']
	'''


	#перевести логическую часть в логику
	#создать часть для работы с БД
	#в основном файле оставить основную часть

if __name__ == '__main__':

	#тесты

	logic = Logic()

	soup = logic.get_soup(logic.url)

	categories = logic.get_categories(soup)
	print('метод: get_categories, тип:', type(categories), categories)

	print('метод: get_pagination_number, тип:', type(logic.get_pagination_number(soup)), logic.get_pagination_number(soup))

	categories_dict = logic.get_categories_dict(soup)
	print('метод: get_categories_dict, тип:', type(categories_dict), categories_dict)
	#categories_dict = {'Scenes': 'https://hub.virtamate.com/resources/categories/scenes.3/', 'Looks': 'https://hub.virtamate.com/resources/categories/looks.7/', 'Clothing': 'https://hub.virtamate.com/resources/categories/clothing.8/', 'Hairstyles': 'https://hub.virtamate.com/resources/categories/hairstyles.9/', 'Morphs': 'https://hub.virtamate.com/resources/categories/morphs.10/', 'Textures': 'https://hub.virtamate.com/resources/categories/textures.11/', 'Plugins': 'https://hub.virtamate.com/resources/categories/plugins.12/', 'Assets': 'https://hub.virtamate.com/resources/categories/assets.2/', 'Guides': 'https://hub.virtamate.com/resources/categories/guides.13/', 'Other': 'https://hub.virtamate.com/resources/categories/other.32/'}


	#для тестов берем только одну категорию, любую
	print('метод: get_pagination_links (на примере одной категории), тип:', type(logic.get_pagination_links(categories_dict.get(categories[7]))), logic.get_pagination_links(categories_dict.get(categories[7]))) #список кусков-страниц одной категории
	#pieces_of_cake = ['https://hub.virtamate.com/resources/categories/scenes.3/?page=1', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=2', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=3', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=4', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=5', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=6', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=7', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=8', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=9', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=10', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=11', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=12', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=13', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=14', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=15', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=16', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=17', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=18', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=19', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=20', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=21', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=22', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=23', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=24', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=25', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=26', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=27', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=28', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=29', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=30', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=31', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=32', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=33', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=34', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=35', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=36', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=37', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=38', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=39', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=40', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=41', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=42', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=43', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=44', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=45', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=46', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=47', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=48', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=49', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=50', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=51', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=52', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=53', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=54', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=55', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=56', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=57']
	pieces_of_cake = ['https://hub.virtamate.com/resources/categories/assets.2?page=1', 'https://hub.virtamate.com/resources/categories/assets.2?page=2', 'https://hub.virtamate.com/resources/categories/assets.2?page=3', 'https://hub.virtamate.com/resources/categories/assets.2?page=4', 'https://hub.virtamate.com/resources/categories/assets.2?page=5', 'https://hub.virtamate.com/resources/categories/assets.2?page=6', 'https://hub.virtamate.com/resources/categories/assets.2?page=7', 'https://hub.virtamate.com/resources/categories/assets.2?page=8', 'https://hub.virtamate.com/resources/categories/assets.2?page=9', 'https://hub.virtamate.com/resources/categories/assets.2?page=10', 'https://hub.virtamate.com/resources/categories/assets.2?page=11', 'https://hub.virtamate.com/resources/categories/assets.2?page=12', 'https://hub.virtamate.com/resources/categories/assets.2?page=13', 'https://hub.virtamate.com/resources/categories/assets.2?page=14', 'https://hub.virtamate.com/resources/categories/assets.2?page=15', 'https://hub.virtamate.com/resources/categories/assets.2?page=16', 'https://hub.virtamate.com/resources/categories/assets.2?page=17', 'https://hub.virtamate.com/resources/categories/assets.2?page=18', 'https://hub.virtamate.com/resources/categories/assets.2?page=19', 'https://hub.virtamate.com/resources/categories/assets.2?page=20', 'https://hub.virtamate.com/resources/categories/assets.2?page=21', 'https://hub.virtamate.com/resources/categories/assets.2?page=22', 'https://hub.virtamate.com/resources/categories/assets.2?page=23', 'https://hub.virtamate.com/resources/categories/assets.2?page=24', 'https://hub.virtamate.com/resources/categories/assets.2?page=25', 'https://hub.virtamate.com/resources/categories/assets.2?page=26', 'https://hub.virtamate.com/resources/categories/assets.2?page=27']

	# для тестов берем только одну ссылку из списка пагинаций (один "кусок пирога"), любой
	card = (logic.get_cards(pieces_of_cake[0]))
	print('метод: get_cards, тип:', type(card), card)

	#!!!устарел!!!
	#print('метод: get_download_link, тип:', type(logic.get_download_link(card['url of content'])), logic.get_download_link(card['url of content']))




	# работа с базой
	# создаем объект базы
	#db = Database()
	'''
	# создаем в базе таблицы с названиями категорий
	for category, link in categories_dict.items():
		#print(category, link)
		#db.create_tables(category)
		#вставляем данные карточки в таблицу
		pagination = logic.get_pagination_links(link)
		print(pagination)
		for piece_of_cake in pagination:
			print(logic.get_cards(piece_of_cake))
			sleep(1)
	'''

	# работа с файлами и папками
	test_card = {'type of content': 'Assets', 'img link': 'https://1387905758.rsc.cdn77.org/data/resource_icons/8/8793.jpg', 'url of content': 'https://hub.virtamate.com/resources/campfire.8793', 'download link': 'https://hub.virtamate.com/resources/campfire.8793/download', 'name': 'Campfire', 'about:': 'Fireplace'}
	download.download(test_card, logic.session, logic.headers, logic.cookies)

# вывод данных таблицы
# db.get_data('Assets')

'''
метод: get_categories, тип: <class 'list'> ['Scenes', 'Looks', 'Clothing', 'Hairstyles', 'Morphs', 'Textures', 'Plugins', 'Assets', 'Guides', 'Other']
метод: get_pagination_number, тип: <class 'int'> 276
метод: get_categories_dict, тип: <class 'dict'> {'Scenes': 'https://hub.virtamate.com/resources/categories/scenes.3', 'Looks': 'https://hub.virtamate.com/resources/categories/looks.7', 'Clothing': 'https://hub.virtamate.com/resources/categories/clothing.8', 'Hairstyles': 'https://hub.virtamate.com/resources/categories/hairstyles.9', 'Morphs': 'https://hub.virtamate.com/resources/categories/morphs.10', 'Textures': 'https://hub.virtamate.com/resources/categories/textures.11', 'Plugins': 'https://hub.virtamate.com/resources/categories/plugins.12', 'Assets': 'https://hub.virtamate.com/resources/categories/assets.2', 'Guides': 'https://hub.virtamate.com/resources/categories/guides.13', 'Other': 'https://hub.virtamate.com/resources/categories/other.32'}
метод: get_pagination_links (на примере одной категории), тип: <class 'list'> ['https://hub.virtamate.com/resources/categories/scenes.3/?page=1', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=2', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=3', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=4', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=5', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=6', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=7', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=8', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=9', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=10', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=11', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=12', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=13', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=14', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=15', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=16', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=17', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=18', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=19', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=20', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=21', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=22', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=23', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=24', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=25', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=26', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=27', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=28', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=29', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=30', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=31', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=32', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=33', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=34', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=35', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=36', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=37', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=38', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=39', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=40', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=41', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=42', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=43', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=44', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=45', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=46', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=47', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=48', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=49', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=50', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=51', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=52', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=53', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=54', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=55', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=56', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=57']
метод: get_cards, тип: <class 'dict'> {'type of content': 'Scenes', 'img link': 'https://1387905758.rsc.cdn77.org/data/resource_icons/13/13339.jpg', 'url of content': 'https://hub.virtamate.com/resources/new-mocap-actress-squirting-uncontrollably-after-her-first-disciplin.13339', 'download link': 'https://hub.virtamate.com/resources/new-mocap-actress-squirting-uncontrollably-after-her-first-disciplin.13339/download', 'name': 'New MoCap Actress Squirting uncontrollably after her first Disciplin', 'about:': 'Scene for VR created by motion capture.'}
метод: get_download_link, тип: <class 'str'> https://hub.virtamate.com/resources/new-mocap-actress-squirting-uncontrollably-after-her-first-disciplin.13339/download
метод: get_pagination_list_all, тип: <class 'list'> ['https://hub.virtamate.com/resources/categories/scenes.3/?page=1', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=2', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=3', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=4', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=5', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=6', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=7', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=8', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=9', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=10', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=11', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=12', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=13', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=14', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=15', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=16', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=17', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=18', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=19', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=20', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=21', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=22', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=23', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=24', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=25', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=26', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=27', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=28', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=29', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=30', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=31', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=32', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=33', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=34', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=35', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=36', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=37', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=38', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=39', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=40', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=41', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=42', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=43', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=44', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=45', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=46', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=47', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=48', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=49', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=50', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=51', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=52', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=53', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=54', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=55', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=56', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=57', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=58', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=59', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=60', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=61', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=62', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=63', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=64', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=65', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=66', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=67', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=68', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=69', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=70', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=71', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=72', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=73', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=74', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=75', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=76', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=77', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=78', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=79', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=80', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=81', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=82', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=83', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=84', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=85', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=86', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=87', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=88', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=89', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=90', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=91', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=92', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=93', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=94', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=95', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=96', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=97', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=98', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=99', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=100', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=101', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=102', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=103', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=104', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=105', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=106', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=107', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=108', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=109', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=110', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=111', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=112', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=113', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=114', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=115', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=116', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=117', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=118', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=119', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=120', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=121', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=122', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=123', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=124', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=125', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=126', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=127', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=128', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=129', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=130', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=131', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=132', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=133', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=134', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=135', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=136', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=137', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=138', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=139', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=140', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=141', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=142', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=143', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=144', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=145', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=146', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=147', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=148', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=149', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=150', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=151', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=152', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=153', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=154', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=155', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=156', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=157', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=158', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=159', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=160', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=161', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=162', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=163', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=164', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=165', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=166', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=167', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=168', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=169', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=170', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=171', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=172', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=173', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=174', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=175', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=176', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=177', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=178', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=179', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=180', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=181', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=182', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=183', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=184', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=185', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=186', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=187', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=188', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=189', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=190', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=191', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=192', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=193', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=194', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=195', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=196', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=197', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=198', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=199', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=200', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=201', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=202', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=203', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=204', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=205', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=206', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=207', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=208', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=209', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=210', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=211', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=212', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=213', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=214', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=215', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=216', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=217', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=218', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=219', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=220', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=221', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=222', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=223', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=224', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=225', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=226', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=227', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=228', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=229', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=230', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=231', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=232', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=233', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=234', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=235', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=236', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=237', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=238', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=239', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=240', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=241', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=242', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=243', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=244', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=245', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=246', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=247', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=248', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=249', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=250', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=251', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=252', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=253', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=254', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=255', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=256', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=257', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=258', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=259', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=260', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=261', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=262', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=263', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=264', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=265', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=266', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=267', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=268', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=269', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=270', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=271', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=272', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=273', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=274', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=275', 'https://hub.virtamate.com/resources/categories/scenes.3/?page=276']
'''

#card = {'type of content': 'Assets', 'img link': 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA', 'url of content': 'https://hub.virtamate.com/resources/heightmeasurethingy.219', 'download link': 'https://hub.virtamate.com/resources/heightmeasurethingy.219/download', 'name': 'HeightMeasureThingy', 'about:': 'This is a stick that can be use to measure things against'}
