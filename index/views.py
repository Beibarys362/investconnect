from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Project
from .forms import ProjectForm
from .models import Feedback

# Главная страница
def index(request):
    feedbacks = Feedback.objects.order_by('-created_at')[:3]
    return render(request, 'index.html', {'feedbacks': feedbacks})
def new_project(request):
    if request.method == 'POST':
        data = request.POST
        file = request.FILES.get('image')
        Project.objects.create(
            category=data.get('category'),
            name=data.get('name'),
            description=data.get('description'),
            image=file,
            required_amount=data.get('required_amount'),
            duration=data.get('duration'),
            roi=data.get('roi') or 0,
            details=data.get('details'),
            tags=data.get('tags'),
            contact_name=data.get('contact_name'),
            contact_email=data.get('contact_email'),
            contact_phone=data.get('contact_phone'),
            website=data.get('website')
        )
        return redirect('project_list')
    return render(request, 'new_project.html')


def project_list(request):
    projects = Project.objects.all()  # Получаем все проекты
    return render(request, 'projects.html', {'projects': projects})
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': project})



def account_view(request):
    form = UserCreationForm()  # ✅ ВСЕГДА создаём form сначала

    if request.method == 'POST':
        if 'password1' in request.POST:
            # Регистрация
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, f"Добро пожаловать, {user.username}!")
                return redirect('index')
            else:
                for error in form.errors.values():
                    messages.error(request, error)
        else:
            # Логин
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"С возвращением, {user.username}!")
                return redirect('index')
            else:
                messages.error(request, "Неверный логин или пароль.")

    return render(request, 'account.html', {'form': form})

def plan_detail(request):
    return render(request, 'plan_detail.html')

from .models import UserSubscription
from django.contrib.auth.decorators import login_required

@login_required
def plan_detail(request):
    if request.method == "POST":
        UserSubscription.objects.update_or_create(
            user=request.user,
            defaults={'is_pro': True}
        )
        messages.success(request, "Вы успешно оформили подписку PRO!")
        return redirect('index')
    return render(request, 'plan_detail.html')


@login_required
def advanced_search(request):
    if not hasattr(request.user, 'usersubscription') or not request.user.usersubscription.is_pro:
        messages.error(request, "Эта функция доступна только для PRO-подписчиков.")
        return redirect('plan_detail')

    projects = Project.objects.all()

    category = request.GET.get('category')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')

    if category:
        projects = projects.filter(category=category)
    if min_amount:
        projects = projects.filter(required_amount__gte=min_amount)
    if max_amount:
        projects = projects.filter(required_amount__lte=max_amount)

    return render(request, 'advanced_search.html', {'projects': projects})


from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required
def analytics_view(request):
    if not hasattr(request.user, 'usersubscription') or not request.user.usersubscription.is_pro:
        messages.error(request, "Доступ к аналитике только для PRO.")
        return redirect('plan_detail')

    from .models import Project

    total_projects = Project.objects.count()
    investors_count = Project.objects.filter(category='investors').count()
    sponsors_count = Project.objects.filter(category='sponsors').count()
    total_amount = Project.objects.aggregate(Sum('required_amount'))['required_amount__sum'] or 0

    context = {
        'total_projects': total_projects,
        'investors_count': investors_count,
        'sponsors_count': sponsors_count,
        'total_amount': total_amount
    }
    return render(request, 'analytics.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


def all_reviews(request):
    feedbacks = Feedback.objects.order_by('-created_at')
    return render(request, 'all_reviews.html', {'feedbacks': feedbacks})

from .models import Feedback

@login_required
def leave_feedback(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        role = request.POST.get("role")
        message = request.POST.get("message")
        rating = int(request.POST.get("rating", 5))

        Feedback.objects.create(
            user=request.user,
            name=name,
            role=role,
            message=message,
            rating=rating
        )

        messages.success(request, "Спасибо за отзыв!")
        return redirect('index')

    return render(request, 'feedback.html')





