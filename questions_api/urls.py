from django.urls import path, include
from rest_framework.routers import DefaultRouter

from questions_api import views

router = DefaultRouter()
router.register('user', views.UserViewSet)
router.register('question', views.QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('resource/', views.GetResourceApiView.as_view()),
]