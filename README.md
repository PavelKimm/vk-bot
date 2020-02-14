Для начала необходимо создать БД с названием vk_bot_db (можно изменить в config.py)
Далее перейти в папку src командой 'cd src'
Выполнить следующие команды
$ python manage.py db init
$ python manage.py db migrate
($ python manage.py db upgrade)

Перед запуском бота необходимо обучить rasa framework, для этого следует перейти в директорию rasa_framework:
$(1)    cd rasa_framework/
и запустить тренировку:
$(1)    rasa train

далее идет запуск framework-а:
$(1)    rasa run --enable-api --cors "*"
в другом терминальном окне создаем туннель из корневой папки:
$(2)    ./ngrok http 5005	(Linux)
$(2)    ngrok.exe http 5005	(Windows)
и записываем его в файл configs.py в переменную rasa_url

далее запускаем сервер для бота (flask_app.py) и в другом терминальном окне создаем туннель:
$(3)    ./ngrok http 5000	(Linux)
$(3)    ngrok.exe http 5000	(Windows)
созданное защищенное соединение нужно предоставить в callback API вконтакте

бот готов к работе