from django.urls import path

from apps.atencion import views

app_name = 'atencion'

urlpatterns = [
    path('', views.ContactoListView.as_view(), name='lista'),
    path('nuevo/', views.ContactoCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.ContactoDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.ContactoUpdateView.as_view(), name='editar'),
]
