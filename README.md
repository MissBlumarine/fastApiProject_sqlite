# fastApiProject_sqlite
В данном проекте реализован простой веб-сервис 
В качестве базы данных используется sqlite.db
Реализованы методы POST, GET (all, by id), PUT, PATCH, DELETE)
Для описанных выше методов присутствуют тесты pytest в файле main_test.py (100% тестов проходят, на отдельной тестовой базе)

Для удобства запуска проект упакован в docker контейнер
Чтобы запустить проект необходимо:
  - в терминале (можно терминале Pycharm) скачать проект с github (git clone {url})
  - в терминале (находясь в папке проекта, где лежит dockerfile) запустить сборку docker контейнера: docker build . -t app
  - затем запустить его командой: docker run -p 8000:8000 -it app
  - перейти по указанной ссылке http://0.0.0.0:8000 в браузер
  - в браузере добавить к вышеуказанному адресу /docs
  - автоматически откроется swagger, в котором можно протестировать все методы.

 - данные в формате json вида: {"id": 1, "software": "string", "version": "string"}
