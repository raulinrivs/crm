from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from filial.models import Filial
from filial.serializers import FilialSerializer


class FilialViewSet(ModelViewSet):
    queryset = Filial.objects.all()
    serializer_class = FilialSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = None
