from rest_framework import serializers
from .models import Stats, TrajOpt
from rest_framework import viewsets
from stats.models_trajopt_profiles import *
import json

class CollisionCostConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollisionCostConfig
        fields = '__all__'


class CollisionConstraintConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollisionConstraintConfig
        fields = '__all__'


class DefaultCompositeProfileSerializer(serializers.ModelSerializer):
    collision_cost_config = CollisionCostConfigSerializer(many=False, read_only=True)
    collision_constraint_config = CollisionConstraintConfigSerializer(many=False, read_only=True)

    class Meta:
        model = TrajOptDefaultCompositeProfile
        fields = '__all__'


class DefaultPlanProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrajOptDefaultPlanProfile
        fields = '__all__'


class BasicTrustRegionSQPParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicTrustRegionSQPParameters
        fields = '__all__'


class DefaultSolverProfileSerializer(serializers.ModelSerializer):
    opt_info = BasicTrustRegionSQPParametersSerializer(many=False, read_only=True)

    class Meta:
        model = TrajOptDefaultSolverProfile
        fields = '__all__'


class TrajOptSerializer(serializers.ModelSerializer):
    default_composite_profile = DefaultCompositeProfileSerializer(many=True, read_only=True)
    default_plan_profile = DefaultPlanProfileSerializer(many=True, read_only=True)
    default_solver_profile = DefaultSolverProfileSerializer(many=True, read_only=True)

    class Meta:
        model = TrajOpt
        fields = '__all__'


class TrajOptViewSet(viewsets.ModelViewSet):
    queryset = TrajOpt.objects.all()
    serializer_class = TrajOptSerializer


class StatSerializer(serializers.ModelSerializer):
    trajopt = TrajOptSerializer(many=False, read_only=True)

    class Meta:
        model = Stats
        fields = '__all__'


class StatViewSet(viewsets.ModelViewSet):
    queryset = Stats.objects.all()
    serializer_class = StatSerializer
