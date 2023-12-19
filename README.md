## API для работы со статистикой для UR5

Для разворачивания нужен доступ к проекту https://github.com/allicen/UR5_Trajopt_UI (закрытый доступ) 
и https://github.com/allicen/UR5_TrajOpt (открытый доступ).

Необходимо запустить UR5_TrajOpt (ROS-проект для работы с роботом-манипулятором) и UR5_Trajopt_UI (Web-интерфейс).

Видео работы приложения: https://www.youtube.com/watch?v=5Q86EpBCiL4

Структура всего проекта:
- ROS Noetic (C++, Python);
- Spring Boot (Java);
- Angular (Typescript);
- Django (Python);
- База данных Mysql (2 базы).

Для разворачивания ROS-окружения используется Docker.

**Схема БД**

1) Для хранения статистики:

<img src="img/db_stat.png" alt="drawing" width="400"/>

2) Для всего остального:

<img src="img/db.png" alt="drawing" width="400"/>


#### Команды для работы с проектом

Создать миграции

```
python3 manage.py makemigrations
```

```
python3 manage.py migrate stats --database=default
```