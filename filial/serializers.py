from rest_framework import serializers
from filial.models import Filial


class FilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = '__all__'
