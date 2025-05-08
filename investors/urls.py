from django.contrib import admin
from django.urls import path
from index import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('account/', views.account_view, name='account'),
    path('new_project/', views.new_project, name='new_project'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('plans/pro/', views.plan_detail, name='plan_detail'),
    path('advanced_search/', views.advanced_search, name='advanced_search'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('feedback/', views.leave_feedback, name='feedback'),      # форма отправки
    path('reviews/', views.all_reviews, name='all_reviews'),       # просмотр отзывов
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
