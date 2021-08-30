from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.main, name='main'),
    path('<int:movie_id>/', views.detail, name='detail'),
    # path('<int:question_id>/', views.detail, name='detail'),    #url 'detail'로 사용
]