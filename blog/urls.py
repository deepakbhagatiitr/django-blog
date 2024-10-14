"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views
from django.conf import settings
# from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from blog.views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.post_list_view, name='home'),  
    path('post/<int:id>/', views.post_details, name='post_detail'),  # Post detail page
    path('about/', views.about, name='about'),  
    path('post/new/', views.create_post, name='create_post'),  # New route for creating a blog post
    path('register/', views.register, name='register'),  
    path('post/<int:id>/delete/', views.post_delete, name='post_delete'),  # Delete post view
    path('post/<int:id>/edit/', views.update_post, name='update_post'),  # Route for updating a post
    path('login/', views.login, name='login'),
    path('author/<str:username>/', views.author_posts_view, name='author_posts'),
    path('logout/', views.logout_view, name='logout'),  
    path('logout_message/', views.logout_message, name='logout_message'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),  # Correctly instantiate the view
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),  # Correctly instantiate the view
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Correctly instantiate the view
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),  # Correctly instantiate the view
    path('profile/', views.profile, name='profile'),  
    path('edit_profile/', views.edit_profile, name='edit_profile'),  
    
]

# Added media URL pattern to serve media files (such as profile images) in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)