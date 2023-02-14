from django.contrib import admin
from .models import Technology, Project, ProjectImage


@admin.action(description="Make projects public")
def make_project_public(modeladmin, request, queryset):
    queryset.update(make_public=True)


@admin.action(description="Make projects private")
def make_project_private(modeladmin, request, queryset):
    queryset.update(make_public=False)


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    ordering = ('name', )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'make_public', 'start_date', 'end_date', 'background_image')
    list_filter = ('tools_used', )
    actions = [make_project_public, make_project_private, ]
    ordering = ('name',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.action(description="Show image")
def show_project_image(modeladmin, request, queryset):
    queryset.update(show=True)


@admin.action(description="Hide image")
def hide_project_image(modeladmin, request, queryset):
    queryset.update(show=False)


class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'show', 'project', 'display_order', 'image', 'upload_time', )
    list_filter = ('project', 'show', )
    ordering = ('project', 'display_order', )
    actions = [show_project_image, hide_project_image, ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


# Register your models here.
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectImage, ProjectImageAdmin)
