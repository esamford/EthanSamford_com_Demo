from django.urls import path
from . import views
urlpatterns = [
    path('', views.project_list, name='projects'),
    path('<id>', views.show_project, name='show project'),
]
