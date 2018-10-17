from rest_framework import status, viewsets, filters, permissions, authentication, generics

from project.settings.common import EMAIL_PROVISIONAL_USER_HOST, EMAIL_PASSWORD_RESET_HOST
from .models import Tag, User, Ladder, Unit, Link, LearningStatus, Comment
from .serializers import TagSerializer, LadderSerializer, UserSerializer, UnitSerializer, LinkSerializer, \
    LearningStatusSerializer, CommentSerializer, ChangePasswordSerializer
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from django.utils import timezone
from datetime import timedelta
from django.template.loader import get_template
from project import settings
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from rest_framework import filters
from functools import reduce
import operator
from django.db.models import Q


def parse_params(words):
    search_words = words.replace('　', ' ').split()
    return search_words


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if type(obj) == User:
            return obj == request.user
        else:
            return obj.user == request.user


class RequestUserPutView(viewsets.ModelViewSet):
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


class LadderViewSet(RequestUserPutView, permissions.BasePermission):
    serializer_class = LadderSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagenation = (LimitOffsetPagination,)

    def get_queryset(self):
        if not self.request.user.id == None:
            queryset = Ladder.objects.all().filter(Q(is_public=True) | Q(user__exact=self.request.user)).distinct()
        else:
            queryset = Ladder.objects.all().filter(is_public=True)

        params = self.request.query_params.get('q', None)

        if params is not None:
            q = parse_params(params)
            query = reduce(operator.and_,
                           (Q(title__icontains=w) | Q(units__description__icontains=w) | Q(units__title__icontains=w)
                            for w in q))
            queryset = queryset.filter(query).distinct()
        return queryset

    @action(methods=['get'], detail=False)
    def ranking(self, request):
        ladder_list = []
        for ladder in Ladder.objects.all():
            ladder_info = {'id': ladder.pk, 'LearningNumber': ladder.count_learning_number()}
            ladder_list.append(ladder_info)

        return Response(sorted(ladder_list, key=lambda x: x['LearningNumber'], reverse=True)[:5])

    @action(methods=['get'], detail=False)
    def trend(self, request):
        ladder_list = []
        for ls in LearningStatus.objects.all().filter(update_at__gte=timezone.now() - timedelta(7)):
            ladder_info = {'id': ls.unit.ladder.pk, 'LearningNumber': ls.unit.ladder.count_learning_number()}
            if ladder_info not in ladder_list:
                ladder_list.append(ladder_info)

        return Response(sorted(ladder_list, key=lambda x: x['LearningNumber'], reverse=True)[:5])


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().filter(is_active=True)
    serializer_class = UserSerializer
    pagenation = (LimitOffsetPagination,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,files=request.files)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        subject = '仮登録完了'
        mail_template = get_template('provisional_user.txt')
        user = User.objects.get(email=request.data['email'])
        token = dumps(user.pk)
        context = {
            'user': user,
            'host': EMAIL_PROVISIONAL_USER_HOST,
            'token': token,
        }
        message = mail_template.render(context)
        from_email = settings.common.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [request.data['email']])

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], detail=True, url_path='learning-ladder')
    def get_learning_ladder(self, request, pk=None):
        ladder_list = []
        for ls in LearningStatus.objects.all().filter(user=pk):
            if ls.ladder.get_learning(user=pk) and ls.unit.index == 1:
                serializer = LadderSerializer(ls.ladder)
                ladder_list.append(serializer.data)

        return Response(ladder_list)

    @action(methods=['get'], detail=True, url_path='finish-ladder')
    def get_finish_ladder(self, request, pk=None):
        ladder_list = []
        for ls in LearningStatus.objects.all().filter(user=pk):
            if ls.ladder.get_finish(user=pk) and ls.unit.index == 1:
                serializer = LadderSerializer(ls.ladder)
                ladder_list.append(serializer.data)

        return Response(ladder_list)

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'create'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=False, url_path='complete')
    def complete_createuser(self, request):
        token = request.GET.get('token')
        try:
            user_pk = loads(token, max_age=settings.common.ACTIVATION_TIMEOUT_SECONDS)
            # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

            # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

            # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoenNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()

                    subject = 'LADDER α版ユーザー登録完了のご案内'
                    mail_template = get_template('mail.txt')
                    context = {'user': user, }
                    message = mail_template.render(context)
                    from_email = settings.common.EMAIL_HOST_USER
                    send_mail(subject, message, from_email, [user.email])
                    serializer = UserSerializer(user)

                    return Response(serializer.data)

        return HttpResponseBadRequest()


class UnitViewSet(RequestUserPutView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    pagenation = (LimitOffsetPagination,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class LinkViewSet(RequestUserPutView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class LearningStatusViewSet(RequestUserPutView):
    serializer_class = LearningStatusSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        queryset = LearningStatus.objects.all()
        user_id = self.request.query_params.get('user', None)
        ladder_id = self.request.query_params.get('ladder', None)

        if user_id is not None:
            queryset = queryset.filter(user=user_id)
        if ladder_id is not None:
            queryset = queryset.filter(unit__ladder=ladder_id)

        return queryset


class CommentViewSet(RequestUserPutView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


@api_view(['POST'])
@permission_classes([AllowAny])
def passreset_mail(request):
    email = request.data['email']
    user = get_object_or_404(User, email=email)
    token = dumps(user.pk)

    subject = 'パスワードリセットの確認'
    mail_template = get_template('password_reset.txt')
    context = {'user': user, 'host': EMAIL_PASSWORD_RESET_HOST, 'token': token}
    message = mail_template.render(context)
    from_email = settings.common.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [user.email])
    serializer = UserSerializer(user)

    return Response({'message': 'send email'})


@api_view(['POST'])
@permission_classes([AllowAny])
def passreset_confirm(request):
    token = request.data['token']
    try:
        user_pk = loads(token, max_age=settings.common.ACTIVATION_TIMEOUT_SECONDS)
        # 期限切れ
    except SignatureExpired:
        return Response({{"message": "token timeout"}}, status=status.HTTP_400_BAD_REQUEST)

        # tokenが間違っている
    except BadSignature:
        return Response({{"message": "token is bad"}}, status=status.HTTP_400_BAD_REQUEST)

        # tokenは問題なし
    else:
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoenNotExist:
            return Response({{"message": "user does not exist"}}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                password_data = request.data['password']
                serializer = UserSerializer(user, data=password_data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                if getattr(user, '_prefetched_objects_cache', None):
                    instance._prefetched_objects_cache = {}

                return Response(serializer.data)
            except:
                return Response({"message": "must set to password"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({{"message": "bad request"}}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'index.html', {})
