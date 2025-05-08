from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, UserSubscription, Feedback  # қажетті модельдерді импорт

admin.site.register(Project)
admin.site.register(UserSubscription)
admin.site.register(Feedback)
