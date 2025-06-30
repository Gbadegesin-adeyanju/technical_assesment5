from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, MarkTaskCompletedView, LoginView, UserView

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/<int:pk>/complete/', MarkTaskCompletedView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', LoginView.as_view(), name='signup'),
]