# Django filters
from django_filters.rest_framework import DjangoFilterBackend
# DRF SimpleJWT
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

# Django
from authentication.models import CustomUser

from authentication.permissions import CustomModelPermissions
# User app
from authentication.models import CustomUser, Funcao
from authentication.serializers import CustomUserSerializer, MyTokenObtainPairSerializer, FuncaoSerializer, \
    CustomUserCreateSerializer
# DRF
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions
from rest_framework.exceptions import ValidationError


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().exclude(is_active=False)
    serializer_class = CustomUserSerializer
    permission_classes = [CustomModelPermissions]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT', 'POST']:
            return CustomUserCreateSerializer
        else:
            return CustomUserSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.associado.id != 1:  # Mudar para um bool em associado para diferenciar a matriz
                return self.queryset.filter(
                    associado_id=self.request.user.associado.id)
        return self.queryset

    def destroy(self, request, pk, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=pk)
            user.is_active = False
            user.save()
            return Response(data={'message': 'Usuário deletado.'}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response(data={'message': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=pk)
            password = request.data.pop('password', None)

            # Update user data using the serializer
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # Save the updates before accessing serializer.data

            # Update the password if provided
            if password:
                user.set_password(password)
                user.save()

            return Response(data={'message': 'Usuário Editado.'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                data={
                    'message': 'Erro na validação dos dados.',
                    'errors': e.args
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except CustomUser.DoesNotExist:
            return Response(data={'message': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                data={'message': 'Erro inesperado.', 'errors': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            funcao = serializer.validated_data['funcao']
            data = serializer.validated_data
            exclude_keys = {"username", "password", "email"}
            kwargs = {key: value for key, value in data.items() if key not in exclude_keys}
            user = CustomUser.objects.create_user(username=username, email=email, password=password, **kwargs)
            return Response(data={'message': 'Usuário criado.'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(
                data={'message': 'Erro na validação dos dados.', 'errors': e.args},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                data={'message': 'Erro inesperado.', 'errors': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class FuncaoViewSet(viewsets.ModelViewSet):
    queryset = Funcao.objects.all()
    serializer_class = FuncaoSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = None
