from rest_framework import status,viewsets,filters,permissions,authentication
from .models import User,Ladder,Unit,Link,LearningStatus,Comment
from .serializers import LadderSerializer,UserSerializer,UnitSerializer,LinkSerializer,LearningStatusSerializer,CommentSerializer
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creater == request.user



class LadderViewSet(viewsets.ModelViewSet,permissions.BasePermission):
    queryset = Ladder.objects.all().filter(is_public=True)
    serializer_class = LadderSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def create(self, request, *args, **kwargs):
        add_data = request.data.copy()
        add_data['creater'] = request.user.pk
        serializer = self.get_serializer(data=add_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        add_data = request.data.copy()
        add_data['creater'] = request.user.pk
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=add_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=['get'],detail=False)
    def ranking(self,request):
        ladder_list = []
        for ladder in Ladder.objects.all():
            ladder_info = {'id':ladder.pk,'LearningNumber':ladder.count_learning_number()}
            ladder_list.append(ladder_info)

        return Response(sorted(ladder_list,key=lambda x: x['LearningNumber'],reverse=True)[:5])

    @action(methods=['get'],detail=False)
    def trend(self,request):
        ladder_list = []
        for ls in LearningStatus.objects.all().filter(update_at__gte=timezone.now()-timedelta(7)):
            ladder_info = {'id':ls.unit.ladder.pk,'LearningNumber':ls.unit.ladder.count_learning_number()}
            if ladder_info not in ladder_list:
                ladder_list.append(ladder_info)

        return Response(sorted(ladder_list,key=lambda x: x['LearningNumber'],reverse=True)[:5])


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('list','retrieve','create'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)


# class TagViewSet(viewsets.ModelViewSet):
#     queryset = Tags.objects.all()
#     serializer_class = TagsSerializer
#
#     def get_permissions(self):
#         if self.action == 'list' or self.action == 'retrieve':
#             permission_classes = [AllowAny]
#         else:
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def create(self, request, *args, **kwargs):
        add_data = request.data.copy()
        add_data['user'] = request.user.pk
        serializer = self.get_serializer(data=add_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        add_data = request.data.copy()
        add_data['user'] = request.user.pk
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=add_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class LearningStatusViewSet(viewsets.ModelViewSet):
    queryset = LearningStatus.objects.all()
    serializer_class = LearningStatusSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    def create(self, request, *args, **kwargs):
        add_data = request.data.copy()
        add_data['user'] = request.user.pk
        serializer = self.get_serializer(data=add_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        add_data = request.data.copy()
        add_data['user'] = request.user.pk
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=add_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    def create(self, request, *args, **kwargs):
        add_data = request.data.copy()
        add_data['user'] = request.user.pk
        serializer = self.get_serializer(data=add_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        add_data = request.data.copy()
        add_data['user'] = request.user.pk
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=add_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)



def index(request):
    return render(request, 'index.html', {})
