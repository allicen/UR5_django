from stats.models_trajopt_profiles import *

class TrajOpt(models.Model):
    # Название исполнителя
    executor_name = models.CharField(max_length=255)

    # Название профиля
    profile_name = models.CharField(max_length=255)

    # Профили планировщика
    default_composite_profile = models.ManyToManyField('stats.TrajOptDefaultCompositeProfile', db_table='trajopt_to_trajopt_default_composite_profile')
    default_plan_profile = models.ManyToManyField('stats.TrajOptDefaultPlanProfile', db_table='trajopt_to_trajopt_default_plan_profile')
    default_solver_profile = models.ManyToManyField('stats.TrajOptDefaultSolverProfile', db_table='trajopt_to_trajopt_default_solver_profile')

    task_name = models.CharField(max_length=255)

    # Программа, которая подается в планировщик для выполнения
    program = models.JSONField(default={'data': []}, null=True)

    class Meta:
        managed = True
        db_table = 'trajopt'


class Stats(models.Model):
    # Дата и время запуска эксперимента
    datetime = models.DateTimeField(auto_now_add=True)

    # Успешно ли прошло построение траектории
    # true - успешно
    # false - провально
    success = models.BooleanField()

    # Время, потраченное на построение траектории
    timer = models.FloatField()

    # Начальное положение робота
    joint_state_start_pose = models.IntegerField()

    # Конечное положение робота
    joint_state_finish_pose = models.IntegerField()

    # Промежуточные проложения робота
    joint_state_middle_poses = models.CharField(max_length=255)

    # Алгоритм построения траектории
    method = models.CharField(max_length=255)

    # Параметры планировщика
    params = models.JSONField()

    # Список препятствий на сцене
    obstacle_group_id = models.IntegerField()

    # Любая дополнительная информация
    note = models.CharField(max_length=255, null=True)

    trajOpt = models.ForeignKey(to=TrajOpt, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'stat'





