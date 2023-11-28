from django.db import models
from django.contrib.postgres.fields import ArrayField


class ContactTestType(models.TextChoices):
  FIRST = 0     # Возврат при первом контакте для любой пары объектов
  CLOSEST = 1   # Возвращает глобальный минимум для пары объектов
  ALL = 2       # Возвращает все контакты для пары объектов
  LIMITED = 3   # Возвращает ограниченный набор контактов для пары объектов


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
    type = models.CharField(choices=CollisionEvaluatorType.choices, default=CollisionEvaluatorType.DISCRETE_CONTINUOUS, max_length=255)

    # Максимальное расстояние, на котором будут оцениваться затраты на столкновение
    safety_margin = models.FloatField(default=0.025)

    # Расстояние за пределами buffer_margin, в котором будет оцениваться оптимизация коллизий.
    # По умолчанию это значение равно 0 (фактически отключено) для учета затрат на коллизии.
    safety_margin_buffer = models.FloatField(0.0)

    # Коэффициент столкновения / вес
    coeff = models.FloatField(20)


class CollisionConstraintConfig(models.Model):
    # Если значение true, к проблеме будет добавлено условие стоимости столкновения. По умолчанию: true
    enabled = models.BooleanField(default=True)

    # Используйте взвешенную сумму для каждой пары связей. Это уменьшает количество уравнений, добавляемых к задаче
    # Если установлено значение true, рекомендуется начинать с коэффициента, равного единице.
    use_weighted_sum = models.BooleanField(False)

    # Тип вычислителя, который будет использоваться для проверки коллизий
    type = models.CharField(choices=CollisionEvaluatorType.choices, default=CollisionEvaluatorType.DISCRETE_CONTINUOUS, max_length=255)

    # Максимальное расстояние, на котором будут оцениваться ограничения на столкновение.
    safety_margin = models.FloatField(default=0.01)

    # Расстояние за пределами safety_margin, на котором будет оцениваться оптимизация столкновения.
    safety_margin_buffer = models.FloatField(default=0.05)

    # Коэффициент столкновения/вес
    coeff = models.FloatField(20)


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
    velocity_coeff = ArrayField( models.CharField(blank=True, max_length=255))

    # Если значение true, то для всех временных шагов будет применена общая стоимость ускорения с целевым значением 0 По умолчанию: false
    smooth_accelerations = models.BooleanField(default=True)

    # Это значение по умолчанию для всех соединений, но позволяет вам взвешивать различные соединения
    acceleration_coeff = ArrayField( models.CharField(blank=True, max_length=255))

    # Если значение true, то для всех временных шагов будет применена стоимость совместного рывка с целевым значением 0 По умолчанию: false
    smooth_jerks = models.BooleanField(default=True)

    # Это значение по умолчанию для всех соединений, но позволяет вам взвешивать различные соединения
    jerk_coeff = ArrayField( models.CharField(blank=True, max_length=255))

    # Если true, применяется стоимость, позволяющая избежать кинематических особенностей
    avoid_singularity = models.BooleanField(default=False)

    # Оптимизация веса, связанная с предотвращением кинематической сингулярности
    avoid_singularity_coeff = models.FloatField(default=5.0)

    # Установите разрешение, при котором необходимо проверить действительность состояния для того, чтобы движение между двумя состояниями было осуществлено
    # будет считаться действительным при последующей проверке траектории, возвращаемой trajopt
    # Разрешение равно longest_valid_segment_fraction * state_space.getMaximumExtent()
    #
    # Примечание: Планировщик придерживается консервативного подхода либо longest_valid_segment_fraction или longest_valid_segment_length.
    longest_valid_segment_fraction = models.FloatField(default=0.01)  # 1%

    # Установите разрешение, при котором необходимо проверить действительность состояния для того, чтобы движение между двумя состояниями было осуществлено
    # чтобы считаться действительным. Если If norm(state1 - state0) > longest_valid_segment_length.
    #
    # Примечание: Это преобразуется в longest_valid_segment_fraction.
    #       longest_valid_segment_fraction = longest_valid_segment_length / state_space.getMaximumExtent()
    longest_valid_segment_length = models.FloatField(default=0.1)

    # Расстояния, стоящие за столкновение специальных звеньев
    special_collision_cost = models.JSONField(default=None)

    # Расстояния, ограничивающие столкновение специальных звеньев
    special_collision_constraint = models.JSONField(default=None)



class TrajOptDefaultPlanProfile(models.Model):
    pass