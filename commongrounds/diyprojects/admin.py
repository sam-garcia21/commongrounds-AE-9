from django.contrib import admin

from .models import Project, ProjectCategory

class ProjectInLine(admin.TabularInline):
    model = Project

class ProjectAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectInLine]

admin.site.register(ProjectCategory, ProjectAdmin)