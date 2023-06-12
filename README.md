# telegram_bot2
Создаем дроплет, устанавливаем на него Ubuntu 22.04

1. Открываем удаленный сервер
	ssh root@138.68.67.244 или с помощью Remmina


2. Копируем реппозиторий
	git clone https://github.com/shibzuko/telegram_bot2.git

3. Создаем переменные окружения
	cd telegram_bot2
	touch .env	#Создаем .env
	chmod 600 .env	# Ограничиваем доступ для просмотра переменных
	nano .env	# Открываем для редактирования-добавляем данные
	
4. Установливаем Python и необходимые зависимости
	sudo apt update
	sudo apt install python3 python3-pip
	
5. Создаем и активируем виртуальное окружение
	sudo apt-get install python3-venv	# Устанавливаем пакет python3-venv
	python3 -m venv env	# Создает виртуальное окружение
	source env/bin/activate	# Активирует виртуальное окружение


6. Затем перейдим в каталог с проектом и установливаем необходимые зависимости с помощью pip:
	pip install -r requirements.txt
	
7. Запуск 
	python main_bot.py
	
Остановить бота Ctrl+C



!!!НО так бот будет работать только до закрытия терминала.

Настройка беспрерывной работы.

1. Перейдите в системную директорию служб systemd:
	cd /etc/systemd/system

2. Создайте файл службы с помощью текстового редактора, например, nano:
	sudo nano my_telegram_bot.service

3. Вставьте содержимое файла службы(ПРИМЕР, ИСПРАВИТЬ ПОД СЕБЯ):
	[Unit] 				# основная часть службы
	Description=My Telegram Bot 	# описание вашего сервиса
	After=network.target 		# указываем, после какого сервиса запускать службу 

	[Service] 			# блок с настройками сервиса
	ExecStart=/root/telegram_bot2/env/bin/python3 /root/telegram_bot2/main_bot.py
	WorkingDirectory=/root/telegram_bot2
	Restart=always 			# указываем, что необходимо автоматически делать рестарт службы в случае отвала
	

	[Install]
	WantedBy=multi-user.target
	
4. Перезапускаем службу
	sudo systemctl daemon-reload
	
	
5. Сохраните(Ctrl+O, Ctrl+X) этот файл в /etc/systemd/system/, например, как /etc/systemd/system/my_telegram_bot.service, затем вы можете использовать команды systemctl для управления службой:
	sudo systemctl enable my_telegram_bot  # запустить бота при старте системы
	sudo systemctl start my_telegram_bot  # запустить бота
	sudo systemctl stop my_telegram_bot  # остановить бота
Проверьте статус службы, чтобы убедиться, что бот успешно запущен:
	sudo systemctl status my_telegram_bot


