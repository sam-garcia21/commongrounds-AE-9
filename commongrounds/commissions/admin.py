from django.contrib import admin

from .models import Commission, CommissionType


class CommissionInline(admin.TabularInline):
    model = Commission


class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType
    inlines = [CommissionInline]


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


admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
