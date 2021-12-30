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
import lxml

base_url = 'https://hub.virtamate.com'
url = 'https://hub.virtamate.com/resources/categories/free.4/?page=1'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}
cookies = {'vamhubconsent': 'yes'}

session = requests.Session()
#r = session.get(url, headers=headers, cookies=cookies) # подсунули свой кук с согласием
#soup = bs(r.content, 'lxml')

#на вход получаем ссылку (str), возвращаем его soup
def get_soup(link):
	r = session.get(link, headers=headers, cookies=cookies) # подсунули свой кук с согласием
	soup = bs(r.content, 'lxml')
	return soup

#получаем число кусков (страниц) бесконечной страницы
def get_pagination_number(soup):
	x = int(soup.find('div', {'class': "menu menu--pageJump", 'data-menu': "menu", 'aria-hidden': "true"}).find('input', {'type': "number"}).get('max'))
	return x


#на вход получаем soup возвращаем категории (dict)
def get_categories_dict(soup):
	cards = soup.find('ol', class_="categoryList toggleTarget is-active").find('li', class_="categoryList-item").find('ol', class_="categoryList toggleTarget is-active")#.find('ol', class_="categoryList toggleTarget is-active"))#.find_all('li', class_="categoryList-item"))
	bards = cards.find_all('li', class_="categoryList-item")

	categories = {}
	for e in bards:
		#<a class="categoryList-link" href="/resources/categories/scenes.3/">
		key = e.find('div', class_="categoryList-itemRow").find('a').text.strip()
		value = base_url + e.find('div', class_="categoryList-itemRow").find('a').get('href')
		categories[key] = value
	return categories

print(get_categories_dict(get_soup(url)))

#на вход получаем ссылку на категорию (строка), возвращаем список кусков (страниц) с контентом согласно пагинации
def get_pagination_list(link :str):
	soup = get_soup(link)
	x = get_pagination_number(soup)
	pagination_list = []
	for i in range(x):
		url = link + '?page={}'.format(i+1)
		pagination_list.append(url)

	return pagination_list

#print(get_pagination_list('https://hub.virtamate.com/resources/categories/plugins.12/'))

#дербаним отрезок на карточки, возвращаем массив
#<div class="structItem structItem--resource is-prefix2  js-inlineModContainer js-resourceListItem-13253" data-author="misterx">
def get_cards(piece_of_cake):
	#piece_of_cake = 'https://hub.virtamate.com/resources/categories/scenes.3/?page=1'
	r = session.get(piece_of_cake, headers=headers, cookies=cookies)
	soup = bs(r.content, 'lxml')
	#print(soup)
	cards = soup.find_all('div', class_="structItem")
	for card in cards:
		#type of content
		print('type of content:', card.find('span', {'class': "label label--silver", 'dir': "auto"}).text)
		#img link
		#'img link:', card.find('img').get('src')
		img_link = card.find('img').get('src')
		x = img_link.rfind('?')
		print('img link:', img_link[:x])
		#url of content
		url_of_content = base_url + card.find('a', {'class': ""}).get('href')
		print('url of content:', url_of_content)
		#download link
		#print('download link:', base_url + get_download_link(url_of_content))
		print('download link:', url_of_content + 'download/')
		#name
		print('name:', card.find('a', {'class': ""}).text)
		#about
		print('about:', card.find('div', class_="structItem-resourceTagLine").text)
		print()

print(get_cards('https://hub.virtamate.com/resources/categories/plugins.12/?page=1'))



#служебный метод. типа паука. для выдергивания ссылки на скачивание. но практика показывает, что достаточно добавить к основной ссылке \download\
def get_download_link(url_of_content):
	#<a href="/resources/version-ii-four-pose-anal.13228/download" class="button--cta button button--icon button--icon--download" data-xf-click="overlay"><span class="button-text">Download</span></a>
	#url_of_content = 'https://hub.virtamate.com/resources/calister-secor-lookalike.13212/'
	r = session.get(url_of_content, headers=headers, cookies=cookies)
	soup = bs(r.content, 'lxml')
	#print(soup)
	download_link = soup.find('a', class_="button--cta").get('href')
	return download_link


#!!!устарело
#получаем категории (list) устарело
def get_categories(soup):
	cards = soup.find('ol', class_="categoryList toggleTarget is-active").find('li', class_="categoryList-item")#.find('ol', class_="categoryList toggleTarget is-active"))#.find_all('li', class_="categoryList-item"))
	bards = cards.find('ol', class_="categoryList toggleTarget is-active").find_all('li', class_="categoryList-item")
	categories = []
	for e in bards:
		categories.append(e.find('div', class_="categoryList-itemRow").find('a').text.strip())
	return categories
	'''
	categories_list = {
		'Scenes': 'https://hub.virtamate.com/resources/categories/scenes.3/',
		'Looks': 'https://hub.virtamate.com/resources/categories/looks.7/',
		'Clothing': 'https://hub.virtamate.com/resources/categories/clothing.8/',
		'Hairstyles': 'https://hub.virtamate.com/resources/categories/hairstyles.9/',
		'Morphs': 'https://hub.virtamate.com/resources/categories/morphs.10/',
		'Textures': 'https://hub.virtamate.com/resources/categories/textures.11/',
		'Plugins': 'https://hub.virtamate.com/resources/categories/plugins.12/',
		'Assets': 'https://hub.virtamate.com/resources/categories/assets.2/',
		'Guides': 'https://hub.virtamate.com/resources/categories/guides.13/',
		'Other': 'https://hub.virtamate.com/resources/categories/other.32/'
		}
	'''
	

#!!!устарел
#получаем ссылки по пагинации (list) сразу на весь бесплатный контент, без отдельной категории (в дальнейшем возможно не понадобится)
def get_pagination_list_all(soup):
	x = int(soup.find('div', {'class': "menu menu--pageJump", 'data-menu': "menu", 'aria-hidden': "true"}).find('input', {'type': "number"}).get('max'))
	print(x)

	pagination_list = []
	for i in range(x):
		#url = 'https://hub.virtamate.com/resources/categories/scenes.3/?page={}&_xfRequestUri=/resources/categories/scenes.3/&_xfWithData=1&_xfToken=1640100032,8b806b61259061428c963fc00b1cf3e4&_xfResponseType=json'.format(i)
		url = 'https://hub.virtamate.com/resources/categories/scenes.3/?page={}'.format(i+1)
		pagination_list.append(url)

	return pagination_list


'''
'https://hub.virtamate.com/resources/categories/plugins.12/?page=1',
'https://hub.virtamate.com/resources/categories/plugins.12/?page=2', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=3', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=4', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=5', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=6', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=7', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=8', 'https://hub.virtamate.com/resources/categories/plugins.12/?page=9']
'''


#перевести логическую часть в логику
#создать часть для работы с БД
#в основном файле оставить основную часть

if __name__ == '__main__':
    pass