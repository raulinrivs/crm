from rest_framework import serializers
from authentication.models import CustomUser, Funcao
from filial.serializers import FilialSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class FuncaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcao
        fields = ['id', 'name']


class CustomUserSerializer(serializers.ModelSerializer):
    associado = FilialSerializer(many=False, read_only=False)
    funcao = FuncaoSerializer(many=False, read_only=False)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'cpf', 'endereco', 'email', 'associado', 'funcao',
        ]


class CustomUserCreateSerializer(serializers.ModelSerializer):
    extra_kwargs = {
        'password': {'write_only': True},
    }

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'cpf', 'endereco', 'email', 'associado', 'funcao', 'password'
        ]

    # def update(self, instance, validated_data):
    #     # Handle associado field update
    #     associado_data = validated_data.pop('associado', None)
    #     if associado_data:
    #         associado_serializer = AssociadoSerializer(instance.associado, data=associado_data, partial=True)
    #         if associado_serializer.is_valid(raise_exception=True):
    #             associado_serializer.save()
    #
    #     # Handle funcao field update (assuming it's a ManyToManyField)
    #     funcao_data = validated_data.pop('funcao', None)
    #     if funcao_data:
    #         funcao_ids = [item['id'] for item in funcao_data]
    #         instance.funcao.set(funcao_ids)
    #
    #     # Update the rest of the fields
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #
    #     # Save the instance
    #     instance.save()
    #
    #     return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['funcao'] = user.funcao.name
        token['associado'] = user.associado.nome
        return token
