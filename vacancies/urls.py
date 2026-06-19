from django.urls import path
from . import views

urlpatterns = [
    path('', views.vacancy_list, name='vacancy_list'),
    path('vacancy/<int:pk>/', views.vacancy_detail, name='vacancy_detail'),
    path('vacancy/add/', views.vacancy_create, name='vacancy_create'),
    path('vacancy/<int:pk>/update/', views.VacancyUpdateView.as_view(), name='vacancy_update'),
    path('vacancy/<int:pk>/delete/', views.VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('parse-jooble/', views.parse_jooble, name='parse_jooble'),
]