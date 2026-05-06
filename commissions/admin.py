from django.contrib import admin

from .models import Commission, CommissionType, Job, JobApplication


class CommissionInline(admin.TabularInline):
    model = Commission


class JobInline(admin.TabularInline):
    model = Job


class JobApplicationInline(admin.TabularInline):
    model = JobApplication


class CommissionAdmin(admin.ModelAdmin):
    model = Commission

    search_fields = ('title',)

    list_display = ('title', 'commission_type',)

    list_filter = ('commission_type', )

    fieldsets = [
        ('Details', {
            'fields': [
                'title', 'commission_type', 'people_required', 'description'
            ]
        })
    ]


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [JobInline]


class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType
    inlines = [CommissionInline]


class JobAdmin(admin.ModelAdmin):
    model = Job
    inlines = [JobApplicationInline]


class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication


admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
