## Jom Match" 
## Описание
Этот проект — веб-приложение на **Django**, готовое к локальному запуску.  
Содержит стандартную структуру Django и позволяет быстро поднять сервер для разработки.
```bash
git clone https://github.com/Dim4ik-creator/test_django.git
cd test_django

#Создаём виртуальное окружение
python -m venv .venv
.venv\Scripts\activate 

# Установка зависимотей
pip install -r requirements.txt

# Выполняем миграции
python manage.py migrate

# Запускаем сервер
python manage.py runserver

После запуска проект будет доступен по адресу:
http://127.0.0.1:8000