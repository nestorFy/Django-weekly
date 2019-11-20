from django.contrib import admin
from .models import Project, ConfWeekly

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'start_date', 'end_date', 'project_create_time')


class WeeklyConfAdmin(admin.ModelAdmin):
    list_display = ('weekly_no', 'weekly_cycle')

admin.site.register(Project, ProjectAdmin)
admin.site.register(ConfWeekly, WeeklyConfAdmin)
