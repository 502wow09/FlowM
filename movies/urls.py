from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.main, name='main'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('learn', views.learn, name='learn'),
    path('search', views.search, name='search'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout_view, name='logout'),
    path('userinfo', views.userinfo, name='userinfo'),
    path('change_pw', views.change_pw, name='change_pw'),
    path('<int:movie_id>/like', views.like, name='like'),

    # path('<int:question_id>/', views.detail, name='detail'),    #url 'detail'로 사용
    # path('learning/', views.learning, name='learning'),
]

