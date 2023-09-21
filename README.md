[Ссылка на образ в Docker Hub](https://hub.docker.com/r/ydtalel/hq-django-app)


[Проект на pythonanywhere](http://ydtalel.pythonanywhere.com/admin/)  
ввести login: user1  
password: 1qazxsw21q  
Далее использовать API маршруты
```
http://ydtalel.pythonanywhere.com/api/lessons/list/
```
```
http://ydtalel.pythonanywhere.com/api/lessons/product/2/
````
```
http://ydtalel.pythonanywhere.com/api/product/stats/
```

## Установка:

1. Клонировать репозиторий: ```git clone https://github.com/Ydtalel/HardQode.git```
2. Установить зависимости: pip install -r requirements.txt
3. Авторизуйтесь перейдя по адресу
```
http://localhost:8000/admin/
```
login: user1  
password: 1qazxsw21q
# запросы через API
Можно использовать готовую коллекцию postman HQ collection.postman_collection.json  
API предоставляет функционал для просмотра информации о продуктах, уроках.  
Для отправления запросов через postman перейдите на вкладку "Authorization" (Аутентификация) в настройках запроса.  
В выпадающем меню "Type" (Тип) выберите "Basic Auth" (Базовая аутентификация).  
Заполните поля "Username" (Имя пользователя) и "Password" (Пароль) вашими данными суперпользователя Django, которые вы использовали при создании суперпользователя с помощью createsuperuser.

## Список Уроков

Этот ресурс предоставляет информацию по всем урокам по всем продуктам к которым пользователь имеет доступ, с выведением информации о статусе и времени просмотра.
### Запрос

```
GET /api/lessons/list/
```
### Ответ

json
```
{
    "title": "Python basics",
    "video_link": "https://www.youtube.com/watch?v=0tM-l_ZsxjU",
    "duration_seconds": 1200,
    "products": [
        {
            "name": "python developer",
            "owner": 1,
            "owner_name": "admin"
        }
    ],
    "viewed": true,
    "view_time_seconds": 1100
}
```
## Список уроков по конкретному продукту

Этот ресурс позволяет получить список уроков по конкретному продукту к которому пользователь имеет доступ, с выведением информации о статусе и времени просмотра, а также датой последнего просмотра ролика.

### Запрос

```
GET /api/lessons/product/{PRODUCT_ID}/
```

### Ответ

json
```
{
    "title": "Git",
    "video_link": "https://www.youtube.com/watch?v=VJm_AjiTEEc",
    "duration_seconds": 8000,
    "products": [
        {
            "name": "python developer",
            "owner": 1,
            "owner_name": "admin"
        },
        {
            "name": "Java developer",
            "owner": 2,
            "owner_name": "user1"
        }
    ],
    "viewed": true,
    "view_time_seconds": 7900
}
```
### Отображение статистики по продуктам

Этот ресурс позволяет получить следующую статистику
- Количество просмотренных уроков от всех учеников.
- Сколько в сумме все ученики потратили времени на просмотр роликов.
- Количество учеников занимающихся на продукте.
- Процент приобретения продукта

### Запрос
```
GET /api/product/stats/
```
### Ответ

json
```
[
    {
        "name": "python developer",
        "total_viewed_lessons": 3,
        "total_view_time": 11200,
        "total_users": 2,
        "purchase_percent": 66.0
    },
    {
        "name": "Java Script",
        "total_viewed_lessons": 1,
        "total_view_time": 12000,
        "total_users": 1,
        "purchase_percent": 33.0
    }
]
```
