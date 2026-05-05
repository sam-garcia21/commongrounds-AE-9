from django.contrib import admin

from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'role',)
    search_fields = ('user__username', 'displaye_name',)
    list_filter = ('role',)


class ProjectInLine(admin.TabularInline):
    model = Project


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectInLine]


class ProjectAdmin(admin.ModelAdmin):
    model = Project


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)

