from rest_framework import routers
from .views import  TagViewSet,UserViewSet, LadderViewSet, UnitViewSet, LinkViewSet, LearningStatusViewSet,CommentViewSet, index
from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'ladder', LadderViewSet,base_name='ladder')
router.register(r'unit', UnitViewSet)
router.register(r'tag', TagViewSet)
router.register(r'link', LinkViewSet)
router.register(r'learningstatus', LearningStatusViewSet,base_name='learningstatus')
router.register(r'comments',CommentViewSet)

urlpatterns = [
    path('api-auth/', obtain_jwt_token),
    path('', index, name='index'),
]
urlpatterns += router.urls
