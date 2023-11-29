from django.db import models


class ContactTestType(models.TextChoices):
    FIRST = 0,  # Возврат при первом контакте для любой пары объектов
    CLOSEST = 1,  # Возвращает глобальный минимум для пары объектов
    ALL = 2,  # Возвращает все контакты для пары объектов
    LIMITED = 3  # Возвращает ограниченный набор контактов для пары объектов


class TermType(models.TextChoices):
    TT_COST = 0x1,  # 00000 0001
    TT_CNT = 0x2,  # 0000 0010
    TT_USE_TIME = 0x4  # 0000 0100


class ModelType(models.TextChoices):
    GUROBI = 'GUROBI',
    OSQP = 'OSQP',
    QPOASES = 'QPOASES',
    BPMPD = 'BPMPD',
    AUTO_SOLVER = 'AUTO_SOLVER'


class CollisionEvaluatorType(models.TextChoices):
    SINGLE_TIMESTEP = 0,
    DISCRETE_CONTINUOUS = 1,
    CAST_CONTINUOUS = 2


class CollisionCostConfig(models.Model):
    # Если значение true, к проблеме будет добавлено условие стоимости столкновения. По умолчанию: true
    enabled = models.BooleanField(default=True)

    # Используйте взвешенную сумму для каждой пары связей. Это уменьшает количество уравнений, добавляемых к задаче
    # Если установлено значение true, рекомендуется начинать с коэффициента, установленного равным единице
    use_weighted_sum = models.BooleanField(default=False)

    # Тип вычислителя, который будет использоваться для проверки на столкновение.
    type = models.CharField(choices=CollisionEvaluatorType.choices, default=CollisionEvaluatorType.DISCRETE_CONTINUOUS,
                            max_length=255)

    # Максимальное расстояние, на котором будут оцениваться затраты на столкновение
    safety_margin = models.FloatField(default=0.025)

    # Расстояние за пределами buffer_margin, в котором будет оцениваться оптимизация коллизий.
    # По умолчанию это значение равно 0 (фактически отключено) для учета затрат на коллизии.
    safety_margin_buffer = models.FloatField(default=0.0)

    # Коэффициент столкновения / вес
    coeff = models.FloatField(default=20)

    class Meta:
        managed = True
        db_table = 'trajopt_collision_cost_config'


class CollisionConstraintConfig(models.Model):
    # Если значение true, к проблеме будет добавлено условие стоимости столкновения. По умолчанию: true
    enabled = models.BooleanField(default=True)

    # Используйте взвешенную сумму для каждой пары связей. Это уменьшает количество уравнений, добавляемых к задаче
    # Если установлено значение true, рекомендуется начинать с коэффициента, равного единице.
    use_weighted_sum = models.BooleanField(False)

    # Тип вычислителя, который будет использоваться для проверки коллизий
    type = models.CharField(choices=CollisionEvaluatorType.choices, default=CollisionEvaluatorType.DISCRETE_CONTINUOUS,
                            max_length=255)

    # Максимальное расстояние, на котором будут оцениваться ограничения на столкновение.
    safety_margin = models.FloatField(default=0.01)

    # Расстояние за пределами safety_margin, на котором будет оцениваться оптимизация столкновения.
    safety_margin_buffer = models.FloatField(default=0.05)

    # Коэффициент столкновения/вес
    coeff = models.FloatField(default=20)

    class Meta:
        managed = True
        db_table = 'trajopt_collision_constraint_config'


class BasicTrustRegionSQPParameters(models.Model):
    improve_ratio_threshold = models.FloatField(null=True)  # минимальное соотношение true_improve/approx_improve
    # принять шаг
    min_trust_box_size = models.FloatField(null=True)  # если область доверия станет еще меньше, выйдите и
    # отчет о сходимости
    min_approx_improve = models.FloatField(null=True)  # если модель улучшается меньше этого, выйдите и
    # отчет о сходимости
    min_approx_improve_frac = models.FloatField(null=True)  # если модель улучшается меньше этого, выйдите и
    # отчет о сходимости
    max_iter = models.FloatField(null=True)  # Максимальное количество итераций
    trust_shrink_ratio = models.FloatField(null=True)  # если улучшение меньше, чем
    # improve_ratio_threshold, сократите область доверия за счет
    # это соотношения
    trust_expand_ratio = models.FloatField(null=True)  # если улучшение меньше, чем
    # improve_ratio_threshold, сократите область доверия за счет
    # это соотношения
    cnt_tolerance = models.FloatField(null=True)  # после сходимости штрафной подзадачи, если
    # нарушение ограничений - это нечто меньшее, чем это, мы закончили

    # Максимальное количество раз, в которое будет увеличена стоимость ограничений
    max_merit_coeff_increases = models.FloatField(null=True)
    # Максимальное количество раз, когда QP-решатель может выйти из строя, прежде чем оптимизация будет прервана
    max_qp_solver_failures = models.IntegerField(null=True)

    merit_coeff_increase_ratio = models.FloatField(
        null=True)  # соотношение, при котором мы увеличиваем коэффициент каждый раз

    # Максимальное время в секундах, в течение которого будет запущен оптимизатор
    max_time = models.FloatField(null=True)

    # Начальный коэффициент, который используется для масштабирования ограничений. Общая стоимость ограничений равна
    # constant_value * coeff * merit_coeff
    initial_merit_error_coeff = models.FloatField(null=True)

    # Если значение true, коэффициенты заслуг будут завышены только для тех ограничений, которые не сработали.
    # Это может помочь, когда ограничений много
    inflate_constraints_individually = models.BooleanField(null=True)
    trust_box_size = models.BooleanField(null=True)  # текущий размер доверительного региона (по компонентам)

    log_results = models.BooleanField(null=True)  # Заносите результаты в файл
    log_dir = models.CharField(max_length=255,
                               null=True)  # Каталог для хранения результатов журнала (по умолчанию: /tmp)

    class Meta:
        managed = True
        db_table = 'trajopt_basic_trust_region_sqp_parameters'


##############################################################
#                                                            #
#                  ПРОФИЛИ ДЛЯ ПЛАНИРОВАНИЯ                  #
#                                                            #
##############################################################

class TrajOptDefaultCompositeProfile(models.Model):
    # Тип контактного теста, который необходимо выполнить: FIRST, CLOSEST, ALL
    contact_test_type = models.CharField(choices=ContactTestType.choices, default=ContactTestType.ALL, max_length=255)

    # Информация о конфигурации для коллизий, которые моделируются как затраты
    collision_cost_config = models.ForeignKey(to=CollisionCostConfig, on_delete=models.CASCADE)

    # Информация о конфигурации для коллизий, которые моделируются как ограничения
    collision_constraint_config = models.ForeignKey(to=CollisionConstraintConfig, on_delete=models.CASCADE)

    # If true, a joint velocity cost with a target of 0 will be applied for all timesteps Default: true
    smooth_velocities = models.BooleanField(default=True)

    # Это значение по умолчанию для всех соединений, но позволяет вам взвешивать различные соединения
    # velocity_coeff = ArrayField(models.CharField(blank=True, max_length=255))
    # velocity_coeff = ArrayField(models.FloatField(), blank=True)
    velocity_coeff = models.JSONField(default={"data": []})

    # Если значение true, то для всех временных шагов будет применена общая стоимость ускорения с целевым значением 0
    # По умолчанию: false
    smooth_accelerations = models.BooleanField(default=True)

    # Это значение по умолчанию для всех соединений, но позволяет вам взвешивать различные соединения
    # acceleration_coeff = ArrayField(models.FloatField(), blank=True)
    acceleration_coeff = models.JSONField(default={"data": []})

    # Если значение true, то для всех временных шагов будет применена стоимость совместного рывка с целевым значением
    # 0 По умолчанию: false
    smooth_jerks = models.BooleanField(default=True)

    # Это значение по умолчанию для всех соединений, но позволяет вам взвешивать различные соединения
    # jerk_coeff = ArrayField(models.FloatField(), blank=True)
    jerk_coeff = models.JSONField(default={"data": []})

    # Если true, применяется стоимость, позволяющая избежать кинематических особенностей
    avoid_singularity = models.BooleanField(default=False)

    # Оптимизация веса, связанная с предотвращением кинематической сингулярности
    avoid_singularity_coeff = models.FloatField(default=5.0)

    # Установите разрешение, при котором необходимо проверить действительность состояния для того, чтобы движение
    # между двумя состояниями было осуществлено будет считаться действительным при последующей проверке траектории,
    # возвращаемой trajopt Разрешение равно longest_valid_segment_fraction * state_space.getMaximumExtent()
    # Примечание: Планировщик придерживается консервативного подхода либо longest_valid_segment_fraction или
    # longest_valid_segment_length.
    longest_valid_segment_fraction = models.FloatField(default=0.01)  # 1%

    # Установите разрешение, при котором необходимо проверить действительность состояния для того, чтобы движение
    # между двумя состояниями было осуществлено чтобы считаться действительным. Если If norm(state1 - state0) >
    # longest_valid_segment_length. Примечание: Это преобразуется в longest_valid_segment_fraction.
    # longest_valid_segment_fraction = longest_valid_segment_length / state_space.getMaximumExtent()
    longest_valid_segment_length = models.FloatField(default=0.1)

    # Расстояния, стоящие за столкновение специальных звеньев
    special_collision_cost = models.JSONField(default=None, null=True)

    # Расстояния, ограничивающие столкновение специальных звеньев
    special_collision_constraint = models.JSONField(default=None, null=True)

    class Meta:
        managed = True
        db_table = 'trajopt_default_composite_profile'


class TrajOptDefaultPlanProfile(models.Model):
    # cartesian_coeff = ArrayField(models.IntegerField(), default=[1, 1, 5], blank=True)
    cartesian_coeff = models.JSONField(default={"data": [1, 1, 5]})

    # joint_coeff = ArrayField(models.IntegerField(), default=[1, 1, 5], blank=True)
    joint_coeff = models.JSONField(default={"data": [1, 1, 5]})

    term_type = models.CharField(choices=TermType.choices, default=TermType.TT_CNT, max_length=255)

    # Не перенесена переменная:
    # Функция ошибки, которая устанавливается в качестве ограничения для каждого временного шага.
    # constraint_error_functions

    class Meta:
        managed = True
        db_table = 'trajopt_default_plan_profile'


class TrajOptDefaultSolverProfile(models.Model):
    # Используемый выпуклый решатель
    convex_solver = models.CharField(choices=ModelType.choices, default=ModelType.OSQP, max_length=255)

    # Конфигурация convex solver для использования, если NULL используются настройки по умолчанию
    convex_solver_config = models.TextField(max_length=10000, default=None, null=True)

    # Параметры оптимизации
    opt_info = models.ForeignKey(to=BasicTrustRegionSQPParameters, on_delete=models.CASCADE)

    # Не перенесена переменная:
    # callbacks

    class Meta:
        managed = True
        db_table = 'trajopt_default_solver_profile'
