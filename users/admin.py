from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # Исправлено имя класса
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_active', 'is_staff')  # Исправлено поле
    search_fields = ('username', 'email', 'first_name',
                     'last_name')  # Поиск по имени и email
    list_filter = ('is_active', 'is_staff')  # Фильтры
    ordering = ('username',)  # Сортировка по алфавиту
