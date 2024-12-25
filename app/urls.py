from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:question_id>', views.question, name='question'),
    path('tag/<str:id_tag>', views.tag, name='tag'),
    path('hot/', views.hot, name='hot'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('like/', views.like, name='like'),
    path('correct/', views.is_correct, name='correct'),
    path('search/', views.search, name="search"),
]
