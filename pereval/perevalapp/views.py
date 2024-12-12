import django_filters
from rest_framework import generics, serializers, filters, viewsets
from .models import Level, Image, User, Coordinate, Pereval
from .serializers import ImageSerializer, CoordSerializer, UserSerializer, LevelSerializer,\
    PerevalSerializer
from rest_framework.response import Response
from rest_framework.views import status
from django_filters import rest_framework as filters


class PerevalFilter(filters.FilterSet):
    user_email = filters.CharFilter(field_name='user__email', lookup_expr='exact')

    class Meta:
        model = Pereval
        fields = ['user_email']

class UserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CoordinateAPIView(generics.ListAPIView):
    queryset = Coordinate.objects.all()
    serializer_class = CoordSerializer


class LevelAPIView(generics.ListAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImageAPIView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class PerevalAPIView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PerevalFilter


    def get_queryset(self):
        queryset = super().get_queryset()
        user_email = self.request.query_params.get('user__email')

        if user_email:
            queryset = queryset.filter(user__email=user_email)

        return queryset


class PerevalDetailAPIView(generics.RetrieveAPIView):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    def get(self, request, pk):
        try:
            pereval = Pereval.objects.get(pk=pk)
            serializer = PerevalSerializer(pereval)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Pereval.DoesNotExist:
            return Response({"message": "Запись не найдена"}, status=status.HTTP_404_NOT_FOUND)


class PerevalUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    def patch(self, request, pk):
        try:
            pereval = Pereval.objects.get(pk=pk)
            if pereval.status != 'new':
                return Response({"state": 0, "message": "Запись не может быть изменена, так как не в статусе 'new'."},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = PerevalSerializer(pereval, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"state": 0, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Pereval.DoesNotExist:
            return Response({"state": 0, "message": "Запись не найдена."}, status=status.HTTP_404_NOT_FOUND)

