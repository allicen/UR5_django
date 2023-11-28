from django.db import models

class Stats(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Дата и время запуска эксперимента
    datetime = models.DateTimeField(null=True)

    # Успешно ли прошло построение траектории
    # true - успешно
    # false - провально
    success = models.BooleanField(null=True)

    # Время, потраченное на построение траектории
    timer = models.FloatField(null=True)

    # Начальное положение робота
    joint_state_start_pose = models.IntegerField(null=True)

    # Конечное положение робота
    joint_state_finish_pose = models.IntegerField(null=True)

    # Промежуточные проложения робота
    joint_state_middle_poses = models.CharField(max_length=255, null=True)

    # Алгоритм построения траектории
    method = models.CharField(max_length=255, null=True)

    # Параметры планировщика
    params = models.JSONField(null=True)

    # Список препятствий на сцене
    obstacle_group_id = models.IntegerField(null=True)

    # Любая дополнительная информация
    note = models.CharField(max_length=255, null=True)

    # class Meta:
    #     managed = False


class TrajOpt(models.Model):
    pass