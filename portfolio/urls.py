"""portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.index, name='index')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='index')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

handler404 = 'exception_handling.views.error_404'
handler500 = 'exception_handling.views.error_500'

urlpatterns = [
    path('', include('index.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('projects/', include('projects.urls'), name="projects"),
    path('contact/', include('contact.urls')),
    path('about/', include('about.urls')),
] + staticfiles_urlpatterns()
