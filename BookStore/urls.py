"""
URL configuration for BookStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from core.views import index, contact, book, signup, add_to_favorites, remove_from_favorites, favorites, logout_view, \
    add_comment, remove_comment, update_comment, update_user, change_password, generate_download_link
from django.contrib.auth import views as auth_views
from core.forms import LoginForm

urlpatterns = [
    path('generate_download_link/<str:book_google_id>', generate_download_link, name='generate_download_link'),
    path('logout/', logout_view, name='logout'),
    path('update_user/', update_user, name='update_user'),
    path('change_password/', change_password, name='change_password'),
    path('update_comment/<int:comment_id>', update_comment, name='update_comment'),
    path('remove_comment/<int:comment_id>', remove_comment, name='remove_comment'),
    path('book/<str:book_google_id>/add_comment/', add_comment, name='add_comment'),
    path('favorites/', favorites, name="favorites"),
    path('remove_from_favorites/<str:book_id>', remove_from_favorites, name="remove_from_favorites"),
    path('add_to_favorites/<str:book_id>', add_to_favorites, name="add_to_favorites"),
    path('book/<str:google_book_id>', book, name="book"),
    path('signin/', auth_views.LoginView.as_view(template_name='core/signin.html', authentication_form=LoginForm), name="signin"),
    path('signup/', signup, name="signup"),
    path('contact/', contact, name="contact"),
    path('', index, name="index"),
    path('admin/', admin.site.urls),
]
