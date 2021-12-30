# Создаем базу
# Создаем таблицы согласно спарсенным категориям
# Загоняем данные карточек пачками с каждого куска каждой категории с проверкой на уникальность

import sqlite3

class Database():
	def __init__(self):
		self.base_url = 'https://hub.virtamate.com'
		self.url = 'https://hub.virtamate.com/resources/categories/free.4/?page=1'
		#db = sqlite3.connect(':memory:')
		self.db = sqlite3.connect('vam_db')
		self.conn = db.cursor()

	# Создаем таблицы согласно категорий
	# На вход принимает категории (dict), создает таблицы с соответствующими именами
	def create_tables(): #(categories :dict)
		#создание таблицы
		tablenames = {'Scenes': 'https://hub.virtamate.com/resources/categories/scenes.3/', 'Looks': 'https://hub.virtamate.com/resources/categories/looks.7/', 'Clothing': 'https://hub.virtamate.com/resources/categories/clothing.8/', 'Hairstyles': 'https://hub.virtamate.com/resources/categories/hairstyles.9/', 'Morphs': 'https://hub.virtamate.com/resources/categories/morphs.10/', 'Textures': 'https://hub.virtamate.com/resources/categories/textures.11/', 'Plugins': 'https://hub.virtamate.com/resources/categories/plugins.12/', 'Assets': 'https://hub.virtamate.com/resources/categories/assets.2/', 'Guides': 'https://hub.virtamate.com/resources/categories/guides.13/', 'Other': 'https://hub.virtamate.com/resources/categories/other.32/'}

		for key, value in tablenames.items():
			try:
				conn.execute('''CREATE TABLE '''+ key + '''(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, about TEXT, contentType TEXT, imgLink TEXT, contentUrl TEXT, downloadLink TEXT)''')	
				#print('Создана таблица ' + key)
			except sqlite3.OperationalError:
				#print('Таблица ' + key + ' уже существует')
				pass

	create_tables()

	#create_tables()

	def set_scenes_data(cards :tuple):
		try:
			sqlite_connection = sqlite3.connect('vam_db')
			cursor = sqlite_connection.cursor()
			print("Подключен к SQLite")

			for card in cards:
				print(card)
				conn.executemany('''INSERT or IGNORE INTO scenes(name, about, contentType, imgLink, contentUrl, downloadLink) VALUES(?,?,?,?,?,?)''', (card,))
				print('Данные добавлены')
				db.commit()
				
		except:
			print("Ошибка при работе с SQLite", error)

		finally:
			if sqlite_connection:
				sqlite_connection.close()
				print("Соединение с SQLite закрыто")






		
			except sqlite3.IntegrityError:
				print(scenes[0][0] + ' уже есть!')
				

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


	def get_scenes_data():
		try:
			sqlite_connection = sqlite3.connect('vam_db')
			cursor = sqlite_connection.cursor()
			print("Подключен к SQLite")

			cursor.execute("""SELECT * from scenes""")
			records = cursor.fetchall()
			print("Вывод каждой строки")
			for row in records:
				print("ID:", row[0])
				print("Имя:", row[1])
				print("Почта:", row[2])
				print("Добавлен:", row[3])
				print("Зарплата:", row[4], end="\n\n")

			cursor.close()

		except sqlite3.Error as error:
			print("Ошибка при работе с SQLite", error)
		finally:
			if sqlite_connection:
				sqlite_connection.close()
				print("Соединение с SQLite закрыто")



	d =[
		['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/3/3134.jpg', 'https://hub.virtamate.com/resources/vammoan.3134/', 'https://hub.virtamate.com/resources/vammoan.3134/download/', 'VAMMoan', 'Add female and male moan or voice related effects to your characters.'], 
		['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/13/13222.jpg', 'https://hub.virtamate.com/resources/bhaviour.13222/', 'https://hub.virtamate.com/resources/bhaviour.13222/download/', 'Bhaviour', 'Make all persons in a scene alive'], ['Plugins', 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA', 'https://hub.virtamate.com/resources/ik-for-custom-unity-assets.12870/', 'https://hub.virtamate.com/resources/ik-for-custom-unity-assets.12870/download/', 'IK for Custom Unity Assets', 'IKCUA'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/12/12663.jpg', 'https://hub.virtamate.com/resources/toyserialcontroller-vamlaunch.12663/', 'https://hub.virtamate.com/resources/toyserialcontroller-vamlaunch.12663/download/', 'ToySerialController+VAMLaunch', 'VAMLaunch controlled by ToySerialController with auto motion sources as a session plugin.'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/13/13003.jpg', 'https://hub.virtamate.com/resources/cue.13003/', 'https://hub.virtamate.com/resources/cue.13003/download/', 'Cue', 'Animations, moods, excitement, breathing, body temperature and gaze.'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/12/12898.jpg', 'https://hub.virtamate.com/resources/iron-grip.12898/', 'https://hub.virtamate.com/resources/iron-grip.12898/download/', 'Iron Grip', 'Customize finger joint physics and colliders to create stronger hands and rigid fingers'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/8/8769.jpg', 'https://hub.virtamate.com/resources/vamatmosphere.8769/', 'https://hub.virtamate.com/resources/vamatmosphere.8769/download/', 'VAMAtmosphere', 'A set of audio tools. Soundscapes, neighbors simulator, thunder simulator, reverb zone'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/11/11994.jpg', 'https://hub.virtamate.com/resources/video-renderer-for-3d-vr180-vr360-and-flat-2d-audio-bvh-animation-recorder.11994/', 'https://hub.virtamate.com/resources/video-renderer-for-3d-vr180-vr360-and-flat-2d-audio-bvh-animation-recorder.11994/download/', 'Video Renderer for 3D VR180, VR360 and Flat 2D & Audio + BVH Animation Recorder', 'Renders 3D VR180, VR360 and flat 2D video & audio and exports BVH skeletal animations'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/0/282.jpg', 'https://hub.virtamate.com/resources/expressionblushingandtears.282/', 'https://hub.virtamate.com/resources/expressionblushingandtears.282/download/', 'ExpressionBlushingAndTears', 'This plugin gives Person a "expression", "tears", and "blush" effect by Collision Triggers.'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/11/11692.jpg', 'https://hub.virtamate.com/resources/animationposer.11692/', 'https://hub.virtamate.com/resources/animationposer.11692/download/', 'AnimationPoser', 'The most powerful random animation plugin to date!'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/12/12286.jpg', 'https://hub.virtamate.com/resources/auto-bulger.12286/', 'https://hub.virtamate.com/resources/auto-bulger.12286/download/', 'Auto Bulger', 'Automatic Belly and Throat Bulge'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/11/11573.jpg', 'https://hub.virtamate.com/resources/kinect360tovam-another-cheap-full-body-tracking-option.11573/', 'https://hub.virtamate.com/resources/kinect360tovam-another-cheap-full-body-tracking-option.11573/download/', 'Kinect360ToVAM - Another cheap full body tracking option', 'Uses a Microsoft XBox 360 Kinect V1.0 3D scanner to provide full body tracking data to VAM'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/10/10672.jpg', 'https://hub.virtamate.com/resources/kinect2vam-full-body-tracking-on-the-cheap.10672/', 'https://hub.virtamate.com/resources/kinect2vam-full-body-tracking-on-the-cheap.10672/download/', 'Kinect2VAM - Full body tracking on the cheap', 'Uses a Microsoft Kinect V2.0 3D scanner to provide full body tracking data to VAM'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/11/11336.jpg', 'https://hub.virtamate.com/resources/benchmark.11336/', 'https://hub.virtamate.com/resources/benchmark.11336/download/', 'Benchmark', 'Measure VaM performance of your PC. Compare with others to make hardware upgrade decisions.'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/3/3493.jpg', 'https://hub.virtamate.com/resources/silver-expression-tool.3493/', 'https://hub.virtamate.com/resources/silver-expression-tool.3493/download/', 'Silver Expression Tool', 'Bring characters to life with two independant series of expressions.'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/8/8269.jpg', 'https://hub.virtamate.com/resources/voicecontrol.8269/', 'https://hub.virtamate.com/resources/voicecontrol.8269/download/', 'VoiceControl', 'A plugin to trigger events via spoken commands.'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/0/94.jpg', 'https://hub.virtamate.com/resources/timeline.94/', 'https://hub.virtamate.com/resources/timeline.94/download/', 'Timeline', 'Create keyframed animations, animate triggers, morphs and much more'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/11/11331.jpg', 'https://hub.virtamate.com/resources/sizeplay-plugins-demo-scenes-included.11331/', 'https://hub.virtamate.com/resources/sizeplay-plugins-demo-scenes-included.11331/download/', 'SizePlay Plugins (Demo Scenes Included)', 'Basic tools for all your giantess/tiny/growth/shrink needs'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/avatars/s/3/3713.jpg', 'https://hub.virtamate.com/resources/desktopclothgrab.11043/', 'https://hub.virtamate.com/resources/desktopclothgrab.11043/download/', 'DesktopClothGrab', 'grab clothing with your mouse pointer in desktop mode'], ['Plugins', 'https://1387905758.rsc.cdn77.org/data/resource_icons/5/5809.jpg', 'https://hub.virtamate.com/resources/desktopleap-use-your-leap-motion-on-desktop.5809/', 'https://hub.virtamate.com/resources/desktopleap-use-your-leap-motion-on-desktop.5809/download/', 'DesktopLeap: Use your Leap Motion on Desktop', 'Use your leap motion for creative or fondling purposes']]

	set_scenes_data(d)
	#get_scenes_data()

	db.close()
if __name__ == '__main__':
	#тесты
	database = Database()
	print(database)