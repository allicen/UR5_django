from rest_framework import serializers
from .models import Stats
from rest_framework import viewsets

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = ('id', 'title', 'description', 'created_at')

class StatViewSet(viewsets.ModelViewSet):
    queryset = Stats.objects.all()
    serializer_class = StatSerializer