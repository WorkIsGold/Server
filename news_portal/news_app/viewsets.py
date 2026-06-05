from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAuthorOrReadOnly
from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from .serializers import UserSerializer, NewsSerializer
from .models import News


class UserViewSet(viewsets.ModelViewSet):

    def get_permission(self):
        if self.action == 'destroy':
            self.permission_classes = [permission.IsAdminUser]
        return super().get_permission()


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['date_created', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)