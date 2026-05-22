from django.urls import path

from apps.cuentas import views

app_name = 'cuentas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.LoginUsuarioView.as_view(), name='login'),
    path('registro/', views.RegistroUsuarioView.as_view(), name='registro'),
    path('logout/', views.logout_usuario, name='logout'),
]
