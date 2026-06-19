from django.db import models

class Vacancy(models.Model):
    title = models.CharField(max_length=255, verbose_name="Назва вакансії")
    company = models.CharField(max_length=255, verbose_name="Компанія")
    location = models.CharField(max_length=255, verbose_name="Місто / Локація")
    salary = models.CharField(
        max_length=100, 
        default="Не вказана", 
        verbose_name="Зарплата"
    )
    description = models.TextField(verbose_name="Опис вакансії")
    source_url = models.URLField(blank=True, null=True, unique=True, verbose_name="Посилання на першоджерело")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = "Вакансія"
        verbose_name_plural = "Вакансії"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company}"