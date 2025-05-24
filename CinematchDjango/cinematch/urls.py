from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='home'),  # Ana sayfa
    path('recommend/', views.recommend_view, name='recommend'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
