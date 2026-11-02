# FlowerShop - сервис доставки букетов

Веб-приложение для заказа букетов. Пользователь может выбрать букет из каталога, пройти квиз для подбора букета под событие и бюджет, оставить заявку на консультацию или оформить заказ с доставкой и оплатой. Заказы и заявки доступны в админке Django. Оплата реализована как учебный сценарий.

## Требования

- Python или Python3 должен быть установлен.

## Быстрый старт

### 1. Виртуальное окружение

Windows, PowerShell:

```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux, macOS:

```
python3 -m venv venv
source venv/bin/activate
```

### 2. Зависимости

```
pip install -r requirements.txt
```

### 3. Переменные окружения

Создайте файл `.env` по примеру `.env.example`:

| Переменная | Обязательна | По умолчанию | Назначение |
| --- | --- | --- | --- |
| `SECRET_KEY` | да | нет | Секретный ключ Django. Без него приложение не стартует |
| `DEBUG` | нет | `True` | Режим отладки. На боевом сервере выставить `False` |
| `ALLOWED_HOSTS` | нет | `127.0.0.1,localhost` | Список доменов через запятую, без пробелов |

### 4. База данных

```
python manage.py migrate
```

### 5. Учётная запись администратора

Нужна, чтобы смотреть заказы и заявки в админке:

```
python manage.py createsuperuser
```

### 6. Запуск

```
python manage.py runserver
```

Сайт откроется на `http://127.0.0.1:8000/`.

## Функционал

- **Главная** - подборка рекомендуемых букетов.
- **Каталог** - все доступные букеты с описанием, составом и ценой.
- **Квиз** - подбор букета под событие и бюджет.
- **Оформление заказа** - указание имени, телефона, адреса, времени доставки, промокод и оплата.
- **Консультация** - заявка флористу на консультацию.
- **Админка** - управление букетами, заказами, промокодами и заявками.

## Линтеры

Для проверки используется [ruff](https://docs.astral.sh/ruff/). Настройки в `pyproject.toml` (длина строки 100, миграции исключены из проверки).

Проверка:

```
ruff check .
ruff format --check .
```

## Развёртывание

Вариант запуска на сервере Linux (без домена) через [gunicorn](https://gunicorn.org/) за обратным прокси [nginx](https://nginx.org/). Статика раздаётся nginx'ом из `STATIC_ROOT`.  

### Порядок действий

Для запуска сайта на сервере Linux должен быть установлен Python3.

1. Разместите проект на сервере, подготовьте окружение
    - Загрузите код проекта на сервер. Например, в папку `/home/имя_проекта/`  
      *Где именно расположить папку с проектом — не самый критичный вопрос, главное — не класть её в директорию, которую напрямую раздаёт веб-сервер (например, в корень Nginx), чтобы избежать утечки исходного кода.*
    - Создайте на сервере новую виртуальную среду Python и установите зависимости:  
      ```bash
      cd /путь/до/проекта
      python3 -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
      pip install gunicorn
      ```
    - Задайте переменные окружения (подробнее в [пункте 3](#3-переменные-окружения))  
      *Для развертывания нужно отключить DEBUG и указать публичный IP вашего сервера в ALLOWED_HOSTS, как в примере:*  
      ```
      SECRET_KEY=REPLACE_ME
      DEBUG=False
      ALLOWED_HOSTS=IP_вашего_сервера,127.0.0.1,.pythonanywhere.com
      ```
    - Cоберите статические файлы (CSS/JS) в одну папку (STATIC_ROOT), которую потом будет раздавать Nginx:  
      ```bash
      python3 manage.py collectstatic
      ```
    - Cоздайте базу данных и учетную запись администратора  
      подробнее в пунктах [4](#4-база-данных) и [5](#5-учётная-запись-администратора)
2. Настройте gunicorn
    - Создайте службу (systemd) для Gunicorn  
      *Чтобы Gunicorn работал постоянно (и перезапускался при падении)*
      ```bash
      nano /etc/systemd/system/gunicorn.service
      ```  
      Вставьте примерно такой текст (пути замените на свои):  
      ```ini
      [Unit]
      Description=gunicorn daemon for Django
      After=network.target
      
      [Service]
      User=ваш_пользователь
      Group=www-data
      WorkingDirectory=/путь/до/папки/с/manage.py
      ExecStart=/путь/до/проекта/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 flower_shop.wsgi:application
      Restart=always
      
      [Install]
      WantedBy=multi-user.target
      ```
    - Затем запустите и включите автозапуск  
      ```bash
      systemctl start gunicorn
      systemctl enable gunicorn
      ```
3. Настройте Nginx
    - Создайте конфиг для вашего сайта:  
      ```bash
      nano /etc/nginx/sites-available/имя_проекта
      ```  
      Вставьте конфигурацию (замените IP и пути):  
      ```nginx
      server {
          listen 80;
          server_name IP_вашего_сервера;
      
          location /static/ {
              alias /путь/до/проекта/staticfiles/;  # куда collectstatic собрал файлы
          }
      
          location /media/ {
              alias /путь/до/проекта/media/;  # Замените на фактический путь MEDIA_ROOT
          }
      
          location / {
              proxy_pass http://127.0.0.1:8000;  # перенаправляем в Gunicorn
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
          }
      }
      ```
    - Включите конфиг и перезагрузите Nginx  
      ```bash
      ln -s /etc/nginx/sites-available/имя_проекта /etc/nginx/sites-enabled/
      
      rm /etc/nginx/sites-enabled/default
      
      nginx -t
      systemctl restart nginx
      ```
4. Настройте файрвол
    - Убедитесь, что открыт порт 80 (HTTP):  
      ```bash
      ufw allow 80
      ```
5. Результат  
   Сайт должен быть доступен по ссылке `http://IP_вашего_сервера`  

7. Обновление кода проекта на сервере  
   После обновления, возможно, понадобится установить новые библиотеки, обновить структуру базы данных, пересобрать статические файлы и перезапустить сервис gunicorn, чтобы сайт обновил свою версию.  

   Чтобы ничего не забыть, выполняйте следующие команды после каждого обновления:  
    ```bash
    pip install -r requirements.txt
    python3 manage.py migrate
    python3 manage.py collectstatic --noinput
    systemctl restart <имя-gunicorn-сервиса>
    ```
