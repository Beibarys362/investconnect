import os
import django

# Установить настройки Django проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investors.settings')
django.setup()

from index.models import Project  # 👈 обязательно правильно путь к модели напиши

def fix_projects():
    for project in Project.objects.all():
        print(f"Проект ID {project.id}: required_amount={project.required_amount}, roi={project.roi}")

        if project.required_amount in ('', None) or project.roi in ('', None):
            print(f"⚠️ Найден битый проект ID {project.id}, исправляем...")

            if not project.required_amount:
                project.required_amount = 0.00

            if not project.roi:
                project.roi = 0.00

            project.save()
            print(f"✅ Проект ID {project.id} успешно исправлен!")

if __name__ == "__main__":
    fix_projects()
