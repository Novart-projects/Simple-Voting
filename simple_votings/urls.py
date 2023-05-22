"""simple_votings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

import web_votings.views as view

urlpatterns = [
    path("auth/", include('users.urls')),
    path("auth/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('', view.get_main_page, name="index"),
    path('list/', view.get_list_of_votings),
    path('vote/<int:id>/', view.show_voitings),
    path('createvote3/<int:id>/', view.create_voting2),
    path('dovote/', view.process_vote),
    path('profile/', view.show_profile),
    path('createvote/', view.show_create_voting),
    path('createvote2/', view.create_voting1),
    path('edit_profile/', view.show_change_profile),
    path('profile_edited/', view.change_profile),
    path('createvote/createvotig/', view.create_voting),
    path('rezults/<int:id>/', view.show_rezs),
    path('edit_voting/<int:id>', view.show_edit_voting),
    path('finish_edit_voting/<int:id>', view.edit_voting),
    path('complaint/<int:id>', view.show_make_complaint),
    path('push_complaint/<int:id>', view.make_complaint),
    path('my_complaint/<int:id>', view.show_complaint),
]
