from django.urls import path

from apps.pacientes import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.PacienteListView.as_view(), name='lista'),
    path('nuevo/', views.PacienteCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.PacienteDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='editar'),
]
