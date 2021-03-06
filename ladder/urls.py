from rest_framework import routers
from .views import TagViewSet, UserViewSet, LadderViewSet, UnitViewSet, LinkViewSet, LearningStatusViewSet, \
    CommentViewSet, passreset_mail, passreset_confirm, UpdatePassword, index
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.urls import path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Lists')

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'ladder', LadderViewSet, base_name='ladder')
router.register(r'unit', UnitViewSet)
router.register(r'tag', TagViewSet)
router.register(r'link', LinkViewSet)
router.register(r'learningstatus', LearningStatusViewSet, base_name='learningstatus')
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('api-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('password/reset/', passreset_mail),
    path('password/reset/confirm/', passreset_confirm),
    path('password/change/', UpdatePassword.as_view()),
    path('', index, name='index'),
    path('swagger/', schema_view),
]
urlpatterns += router.urls
