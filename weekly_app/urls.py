# -*- coding: utf-8 -*-
from django.urls import path
from . import views, expansions

urlpatterns = [
    path(r'', views.LoginView.as_view(), name='login'),
    path(r'index/', views.index, name='index'),
    path(r'logout/', expansions.logout, name='logout'),
    path(r'weekly/', views.weekly_index, name='weekly_index'),
    path(r'weekly_content_view/<str:weekly_id>/', views.weekly_content_view, name="weekly_content_view"),
    path(r'settings/<str:set_type>/', views.settings, name='settings'),

    # Edit
    path(r'alter/<str:alter_type>/<str:alter_id>/', views.alter, name='alter'),

    # Project
    # path('project_view/', views.project_view, name="project_view"),
    path('project_view/', views.ProjectViewClass.as_view(), name="project_view"),
    path('project_edit/<str:edit_type>/', views.project_edit, name="project_edit"),

    # Weekly
    path('weekly_list/', views.weekly_list, name="weekly_list"),
    path('weekly_content_writting/', views.weekly_content_writting, name="weekly_content_writting"),
    path('weekly_content_view/<str:weekly_id>/', views.weekly_content_writting, name="weekly_content_writting"),
]
