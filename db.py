# Создаем базу
# Создаем таблицы согласно спарсенным категориям
# Загоняем данные карточек пачками с каждого куска каждой категории с проверкой на уникальность

import sqlite3

class Database():
	def __init__(self):
		self.base_url = 'https://hub.virtamate.com'
		self.url = 'https://hub.virtamate.com/resources/categories/free.4/?page=1'
		#db = sqlite3.connect(':memory:')
		db = sqlite3.connect('vam_db')
		self.conn = sqlite3.connect('vam_db')
		print("Подключен к SQLite")
		# Создаем курсор - это специальный объект который делает запросы и получает их результаты
		self.cursor = self.conn.cursor()





	# Создаем таблицы согласно категорий
	# На вход принимает категорию (str), создает таблицу с соответствующим именем
	def create_tables(self, tablename :str): #(categories :dict)
		#создание таблицы
		#tablenames = {'Scenes': 'https://hub.virtamate.com/resources/categories/scenes.3/', 'Looks': 'https://hub.virtamate.com/resources/categories/looks.7/', 'Clothing': 'https://hub.virtamate.com/resources/categories/clothing.8/', 'Hairstyles': 'https://hub.virtamate.com/resources/categories/hairstyles.9/', 'Morphs': 'https://hub.virtamate.com/resources/categories/morphs.10/', 'Textures': 'https://hub.virtamate.com/resources/categories/textures.11/', 'Plugins': 'https://hub.virtamate.com/resources/categories/plugins.12/', 'Assets': 'https://hub.virtamate.com/resources/categories/assets.2/', 'Guides': 'https://hub.virtamate.com/resources/categories/guides.13/', 'Other': 'https://hub.virtamate.com/resources/categories/other.32/'}
		try:
			#test_card = {'type of content': '', 'img link': '', 'url of content': '', 'download content link': '', 'download depensies link': None, 'name': '', 'about': ''}
			self.conn.execute('''CREATE TABLE ''' + tablename + '''(id INTEGER PRIMARY KEY AUTOINCREMENT, 
																	TypeOfContent TEXT, 
																	ImgLink TEXT, 
																	UrlOfContent TEXT, 
																	ImgLink TEXT, 
																	DownloadContentLink TEXT, 
																	DownloadDependenciesLink TEXT, 
																	Name TEXT UNIQUE)''')
			print('Создана таблица ' + tablename)
		except sqlite3.OperationalError:
			print('Таблица ' + tablename + ' уже существует')

		# Не забываем закрыть соединение с базой данных
		self.conn.close()

	def set_data(self, card: dict):
		# 'type of content': 'Scenes',
		# 'img link': 'https://1387905758.rsc.cdn77.org/data/resource_icons/11/11561.jpg',
		# 'url of content': 'https://hub.virtamate.com/resources/bj-fantasy.11561',
		# 'download content link': 'https://hub.virtamate.com/resources/bj-fantasy.11561/download',
		# 'download dependencies link': None,
		# 'name': 'BJ Fantasy',
		# 'about': 'SR6 optimized BJ with Voice Control and LOTS of randomized animations plus huge video screens'
		category = card.get('type of content')
		print('Метод db.set_data: В присланной карточке находится категория', category)
		#try:
		print('Вносим', card.get('name'))
		#TypeOfContent TEXT, ImgLink TEXT, UrlOfContent TEXT, ImgLink TEXT, DownloadContentLink TEXT, DownloadDependenciesLink TEXT, Name TEXT UNIQUE)
		self.conn.execute('''INSERT or IGNORE INTO ''' + category + '''(TypeOfContent, 
																	ImgLink,
																	UrlOfContent,
																	DownloadContentLink,
																	DownloadDependenciesLink,
																	Name,
																	About, 
																	) VALUES(?,?,?,?,?,?,?)''', (card,))
		self.conn.commit()
		print('Данные добавлены')

		#Не забываем закрыть соединение с базой данных
		self.conn.close()

		#except:
		#	print("Ошибка при работе с SQLite")

		#finally:
		#	if sqlite_connection:

		# Не забываем закрыть соединение с базой данных
		#self.conn.close()
		#		print("Соединение с SQLite закрыто")


			#except sqlite3.IntegrityError:
			#	print(scenes[0][0] + ' уже есть!')
				

	def set_looks_data(card :tuple):
		pass
	def set_clothing_data(card :tuple):
		pass
	def set_hairstyles_data(card :tuple):
		pass
	def set_morphs_data(card :tuple):
		pass
	def set_textures_data(card :tuple):
		pass
	def set_plugins_data(card :tuple):
		pass
	def set_assets_data(card :tuple):
		pass
	def set_guides_data(card :tuple):
		pass
	def set_other_data(card :tuple):
		pass

	def get_data(self, table):
		sqlite_connection = sqlite3.connect('vam_db')
		cursor = sqlite_connection.cursor()
		print("Подключен к SQLite")

		print("Таблица", table)

		cursor.execute("""SELECT * from """ + table)
		records = cursor.fetchall()
		print("Вывод каждой строки")
		for row in records:
			print("name:", row[0])
			print("about:", row[1])
			print("contentType:", row[2])
			print("imgLink:", row[3])
			print("contentUrl:", row[4])
			print("downloadLink:", row[5], end="\n\n")

		cursor.close()



if __name__ == '__main__':
	#тесты
	database = Database()
	print(database)