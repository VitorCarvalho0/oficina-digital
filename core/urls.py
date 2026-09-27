from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.criar_conta, name='criar_conta'),
    path('login/', views.fazer_login, name='fazer_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
