from django.contrib import admin
from .models import Vacancy

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'salary', 'created_at')
    search_fields = ('title', 'company', 'description')
    list_filter = ('location', 'created_at')