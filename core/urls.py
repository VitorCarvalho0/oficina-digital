from django.urls import path
from . import views

urlpatterns = [
    path('', views.fazer_login, name='fazer_login'),
    path('login/', views.fazer_login, name='fazer_login'),
    path('cadastro/', views.criar_conta, name='criar_conta'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('novo/', views.novo_atendimento, name='novo_atendimento'),
    path('atendimento/<int:pk>/', views.detalhe_atendimento, name='detalhe_atendimento'),
    path('atendimento/<int:pk>/pdf/', views.gerar_pdf_atendimento, name='gerar_pdf_atendimento'),
    path('status/<uuid:token>/', views.acompanhar_atendimento, name='acompanhar_atendimento'),
]
