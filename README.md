## API для работы со статистикой для UR5

Для разворачивания нужен доступ к проекту https://github.com/allicen/UR5_Trajopt_UI (закрытый доступ) 
и https://github.com/allicen/UR5_TrajOpt (открытый доступ).

Необходимо запустить UR5_TrajOpt (ROS-проект для работы с роботом-манипулятором) и UR5_Trajopt_UI (Web-интерфейс).



#### Команды для работы с проектом

Создать миграции

```
python3 manage.py makemigrations
```

```
python3 manage.py migrate stats --database=default
```