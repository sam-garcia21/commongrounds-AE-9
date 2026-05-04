from django.contrib import admin

from .models import Project, ProjectCategory


class ProjectInLine(admin.TabularInline):
    model = Project


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectInLine]


class ProjectAdmin(admin.ModelAdmin):
    model = Project


admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)


class ProjectAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectInLine]


admin.site.register(ProjectCategory, ProjectAdmin)