from django.db import models  # Импорт
from decimal import Decimal
from django.contrib.auth.models import User
class Project(models.Model):
    CATEGORY_CHOICES = [
        ('sponsors', 'Для спонсоров'),
        ('investors', 'Для инвесторов'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='investors')
    name = models.CharField(max_length=255, default='Без названия')
    description = models.TextField(default='Описание проекта отсутствует')
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    required_amount = models.IntegerField(default=0)

    duration = models.IntegerField(help_text="Срок реализации в месяцах", default=6)  # Добавлено дефолтное значение
    roi = models.IntegerField(null=True, blank=True, default=0)

    # Обязательное поле, но с дефолтным значением
    details = models.TextField(default='Опишите ваш проект подробно цели, задачи, этапы реализации, команда', blank=False)

    # Сделано необязательным или с дефолтным значением
    tags = models.CharField(max_length=255, blank=True, default='')

    contact_name = models.CharField(max_length=100, default='Не указано')  # Добавлен дефолт
    contact_email = models.EmailField(default='example@example.com')  # Добавлен дефолт
    contact_phone = models.CharField(max_length=20, blank=True, default='Не указан')
    website = models.URLField(blank=True, default='https://example.com')  # Добавлен дефолт
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



from django.contrib.auth.models import User
from django.db import models

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_pro = models.BooleanField(default=False)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - PRO: {self.is_pro}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating}★)"




