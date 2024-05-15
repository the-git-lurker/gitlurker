"""
URL configuration for Three_Sentences_or_Less project.

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
from . import views

app_name = 'git_lurker'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Home Page
    path("", views.index, name="index"),
    # Individual Project Page
    path("<slug:owner>/project", views.project_view, name="project"),
    # Individual release Page
    path("<slug:owner>/<path:repo>/latest", views.release_view, name="release"),
    # Individual Repo Page
    path("<slug:owner>/<path:repo>/repo", views.repository_view, name="repository"),
    # Support Page
    path("support/", views.support_view, name="support"),
]

handler404 = "git_lurker.views.page_not_found_view"