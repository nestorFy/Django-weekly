"""weeklyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # 项目列表显示
    # path('project/', views.project, name='project'),
    path('project/', views.ProjectView.as_view(), name='project'),
    # 增加一个项目
    # path('project_add/', views.project_add, name='project_add'),
    path('project_add/', views.ProjectCreateView.as_view(), name='project_add'),
    # 编辑现有条目
    path('project_edit/<int:project_id>/', views.ProjectUpdateView.as_view(), name='project_edit'),
    # 删除一个项目
    path('project_delete/<int:pk>/', views.ProjectDeleteView.as_view(), name='project_delete'),

    # 周报配置url
    path('conf_weekly/', views.ConfWeeklyView.as_view(), name='conf_weekly'),
    path('conf_weekly_add/', views.ConfWeeklyCreateView.as_view(), name='conf_weekly_add'),


]
